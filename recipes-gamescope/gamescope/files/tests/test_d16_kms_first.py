#!/usr/bin/env python3
"""Exercise production D16 seat-before-ICD ordering and node verification."""
import pathlib, subprocess, sys, tempfile, unittest, importlib.machinery, os
from unittest import mock
SOURCE=pathlib.Path(sys.argv.pop(1)); SESSION=pathlib.Path(sys.argv.pop(1))
def extract(text,marker):
 start=text.index(marker);body=text.index("{",start);depth=1;end=body+1
 while depth:depth+=(text[end]=="{")-(text[end]=="}");end+=1
 return text[start:end]
class D16KmsFirstTest(unittest.TestCase):
 def test_real_node_helpers_reject_unverified_devices_and_free_metadata(self):
  source=(SOURCE/"drm.cpp").read_text()
  harness=r"""
#include <sys/stat.h>
#include <cstring>
#include <cstdlib>
#include <cassert>
struct drm_t { char *device_name=nullptr; };
struct drmDevice { int available_nodes; }; struct drmVersion { char *name; };
static constexpr int DRM_NODE_PRIMARY=0,DRM_NODE_RENDER=2;
static int scenario, allocations;
static const char *fakeEnv(const char *s) {
 if(!strcmp(s,"ROWANOS_D16_SINGLE_GPU"))return scenario==1?nullptr:scenario==2?"0":"1";
 if(!strcmp(s,"ROWANOS_DRM_RENDER_NODE"))return scenario==3?"/dev/dri/renderD129":"/dev/dri/renderD128";
 if(!strcmp(s,"ROWANOS_DRM_PRIMARY_NODE"))return scenario==4?"/dev/dri/card1":"/dev/dri/card0";
 return nullptr;
}
static int fakeStat(const char*s,struct stat*out){
 if(scenario==5)return -1;
 out->st_mode=scenario==6?S_IFREG:S_IFCHR;
 out->st_rdev=strstr(s,"render")?128:0;return 0;
}
static int fakeFstat(int fd,struct stat*out){assert(fd==9);if(scenario==10)return -1;out->st_mode=S_IFCHR;out->st_rdev=scenario==11?1:0;return 0;}
static int drmGetDeviceFromDevId(dev_t id,int,drmDevice **out){
 if(scenario==7&&id==0)return -1;
 *out=new drmDevice{scenario==8?0:(id==128?4:1)};++allocations;return 0;
}
static bool drmDevicesEqual(drmDevice*,drmDevice*){return scenario!=9;}
static void drmFreeDevice(drmDevice**p){assert(*p);delete *p;*p=nullptr;--allocations;}
static drmVersion *drmGetVersion(int fd){assert(fd==9);if(scenario==12)return nullptr;++allocations;return new drmVersion{const_cast<char*>(scenario==13?"other":"mediatek")};}
static void drmFreeVersion(drmVersion*v){delete v;--allocations;}
struct Log { template<class...T>void errorf(const char*,T...){} }drm_log;
#define getenv fakeEnv
#define stat(...) fakeStat(__VA_ARGS__)
#define fstat(...) fakeFstat(__VA_ARGS__)
"""
  harness+=extract(source,"static bool selectD16EarlyPrimaryNode(")
  harness+=extract(source,"static bool validateD16EarlyKmsFd(")
  harness+=r"""
int main(){
 for(scenario=0;scenario<=13;scenario++){
  drm_t d;bool selected=selectD16EarlyPrimaryNode(&d);
  assert(selected==(scenario==0||scenario>=10));assert(allocations==0);
  if(selected){assert(!strcmp(d.device_name,"/dev/dri/card0"));free(d.device_name);}
  bool fdOk=validateD16EarlyKmsFd(9);assert(fdOk==(scenario<10&&scenario!=5&&scenario!=6));assert(allocations==0);
 }
}
"""
  self.compile_run(harness)
 def test_production_startup_order_and_single_output_init(self):
  text=(SOURCE/"main.cpp").read_text()
  start=text.index('\tconst char *kmsFirst = getenv("ROWANOS_D16_KMS_FIRST");')
  end=text.index('\tVkSurfaceKHR surface',start)
  early=text[start:end]
  start=text.index('\tif ( !d16KmsFirst && !initOutput(')
  end=text.index('\n\tif ( BIsSDLSession()',start)
  normal=text[start:end]
  harness=r"""
#include <cstdlib>
#include <cstring>
#include <cassert>
#include <cstdio>
using VkInstance=void*;
#define VK_NULL_HANDLE nullptr
static bool nested,optIn, outputOk,instanceOk;static int outputCount,instanceCount,events;
static int g_nPreferredOutputWidth=1920,g_nPreferredOutputHeight=1080,g_nNestedRefresh=60;
static const char *fakeEnv(const char*){return optIn?"1":nullptr;}
#define getenv fakeEnv
static bool BIsNested(){return nested;}
static bool initOutput(int,int,int){++outputCount;if(optIn&&!nested)assert(instanceCount==0);else assert(instanceCount==1);events=1;return outputOk;}
static VkInstance vulkan_create_instance(){++instanceCount;if(optIn&&!nested)assert(events==1);else assert(outputCount==0);return instanceOk?(void*)1:nullptr;}
static int startup(){
"""
  harness+=early+normal+'return 0;\n}\n'
  harness+=r"""
int main(){
 for(int n=0;n<2;n++)for(int o=0;o<2;o++)for(int out=0;out<2;out++)for(int inst=0;inst<2;inst++){
  nested=n;optIn=o;outputOk=out;instanceOk=inst;outputCount=instanceCount=events=0;
  assert(startup()==((out&&inst)?0:1));
  if(optIn&&!nested){assert(outputCount==1);assert(instanceCount==(out?1:0));}
  else {assert(instanceCount==1);assert(outputCount==(inst?1:0));}
 }
}
"""
  self.compile_run(harness)
 def test_session_passes_logind_and_explicit_kms_first_mapping(self):
  module=importlib.machinery.SourceFileLoader("rowanos_session_review",str(SESSION)).load_module()
  with tempfile.TemporaryDirectory() as td:
   env={"XDG_RUNTIME_DIR":td,"ROWANOS_SESSION_BACKEND":"gamescope-drm"}
   with mock.patch.dict(os.environ,env,clear=True), mock.patch.object(module.os,"geteuid",return_value=1000), mock.patch.object(module.os,"execv",side_effect=SystemExit) as execute:
    with self.assertRaises(SystemExit):module.user_session()
    self.assertEqual(execute.call_args[0][0],"/usr/bin/gamescope")
    self.assertEqual(os.environ["LIBSEAT_BACKEND"],"logind")
    self.assertEqual(os.environ["ROWANOS_D16_KMS_FIRST"],"1")
    self.assertEqual(os.environ["ROWANOS_D16_SINGLE_GPU"],"1")
    self.assertEqual(os.environ["ROWANOS_DRM_PRIMARY_NODE"],"/dev/dri/card0")
    self.assertEqual(os.environ["ROWANOS_DRM_RENDER_NODE"],"/dev/dri/renderD128")
 def compile_run(self,source):
  with tempfile.TemporaryDirectory() as td:
   path=pathlib.Path(td);(path/"test.cpp").write_text(source)
   subprocess.run(["g++","-std=c++14","-Wall","-Wextra",str(path/"test.cpp"),"-o",str(path/"test")],check=True)
   subprocess.run([str(path/"test")],check=True)
if __name__=="__main__":unittest.main()
