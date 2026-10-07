#!/usr/bin/env python3
"""Exercise actual dumb BO metadata/PRIME lifetime and modifier import helpers."""
import pathlib, shutil, subprocess, sys, tempfile, unittest
SOURCE=pathlib.Path(sys.argv.pop(1)); INCLUDE=pathlib.Path(sys.argv.pop(1))
def extract(source,marker):
 start=source.find(marker)
 if start<0: raise AssertionError("Missing production helper: "+marker)
 body=source.index("{",start); end=body+1; depth=1
 while depth:
  depth+=(source[end]=="{")-(source[end]=="}"); end+=1
 return source[start:end]+(";" if marker.startswith("class ") else "")
class DumbImportTest(unittest.TestCase):
 def test_metadata_bounds_gem_and_fd_lifetime(self):
  helpers="\n".join(extract(SOURCE.read_text(),m) for m in ("class D16ScopedFd","static bool validD16LinearLayout(","class D16ScopedDumb","static bool createD16DumbBuffer(","static bool importD16DumbMemory("))
  harness=r'''
#include <vulkan/vulkan_core.h>
#include <xf86drm.h>
#include <drm_mode.h>
#include <unistd.h>
#include <fcntl.h>
#include <utility>
#include <cassert>
#include <cstdint>
#include <climits>
#include <set>
static int scenario, nextFd, destroyCount; static bool gem;
static std::set<int> owned;
static int fakeClose(int fd){assert(owned.erase(fd)==1);return 0;}
static int fakeFcntl(int fd,int cmd,int){assert(owned.count(fd)&&cmd==F_DUPFD_CLOEXEC);if(scenario==8)return -1;owned.insert(++nextFd);return nextFd;}
static int fakeDrmIoctl(int fd,unsigned long op,void *arg){
 assert(fd==3);
 if(op==DRM_IOCTL_MODE_CREATE_DUMB){
  auto a=static_cast<drm_mode_create_dumb *>(arg);assert(a->width==1920&&a->height==1080&&a->bpp==32);
  if(scenario==1)return -1; gem=true;a->handle=7;a->pitch=scenario==2?7679:7680;a->size=scenario==3?4096:8294400;return 0;
 }
 assert(op==DRM_IOCTL_MODE_DESTROY_DUMB&&gem);auto a=static_cast<drm_mode_destroy_dumb *>(arg);assert(a->handle==7);gem=false;++destroyCount;return 0;
}
static int fakePrime(int fd,uint32_t handle,uint32_t flags,int *out){
 assert(fd==3&&handle==7&&gem&&flags==(DRM_CLOEXEC|DRM_RDWR));
 if(scenario==4)return -1;owned.insert(++nextFd);*out=nextFd;return 0;
}
static off_t fakeLseek(int fd,off_t,int){assert(owned.count(fd));return scenario==5?4096:8294400;}
#define close fakeClose
#define fcntl fakeFcntl
#define drmIoctl fakeDrmIoctl
#define drmPrimeHandleToFD fakePrime
#define lseek fakeLseek
static VkResult fdProps(VkDevice,VkExternalMemoryHandleTypeFlagBits type,int fd,VkMemoryFdPropertiesKHR *out){
 assert(type==VK_EXTERNAL_MEMORY_HANDLE_TYPE_DMA_BUF_BIT_EXT&&owned.count(fd));if(scenario==6)return VK_ERROR_INVALID_EXTERNAL_HANDLE;
 out->memoryTypeBits=scenario==7?2:5;return VK_SUCCESS;
}
static VkResult alloc(VkDevice,const VkMemoryAllocateInfo *info,const VkAllocationCallbacks *,VkDeviceMemory *out){
 assert(info->allocationSize==8294400&&info->memoryTypeIndex==2);
 auto imp=static_cast<const VkImportMemoryFdInfoKHR *>(info->pNext);assert(imp->sType==VK_STRUCTURE_TYPE_IMPORT_MEMORY_FD_INFO_KHR&&imp->handleType==VK_EXTERNAL_MEMORY_HANDLE_TYPE_DMA_BUF_BIT_EXT);
 auto dedicated=static_cast<const VkMemoryDedicatedAllocateInfo *>(imp->pNext);assert(dedicated->image==(VkImage)1&&!dedicated->pNext);
 if(scenario==9)return VK_ERROR_OUT_OF_DEVICE_MEMORY;assert(owned.erase(imp->fd)==1);*out=(VkDeviceMemory)42;return VK_SUCCESS;
}
struct Device{struct Dispatch{decltype(&fdProps)GetMemoryFdPropertiesKHR=fdProps;decltype(&alloc)AllocateMemory=alloc;}vk;
 VkDevice device(){return VK_NULL_HANDLE;}int32_t findMemoryType(VkMemoryPropertyFlags,uint32_t bits){return bits&4?2:-1;}}g_device;
struct Log{template<class...T>void errorf(const char *,T...){}template<class...T>void errorf_errno(const char *,T...){}template<class...T>void infof(const char *,T...){}}vk_log;
static void vk_errorf(VkResult,const char *){}
'''
  harness+=helpers
  harness+=r'''
int main(){
 for(scenario=0;scenario<=9;++scenario){
  nextFd=10;destroyCount=0;gem=false;owned.clear();int fd=-1;VkSubresourceLayout layout={};VkDeviceSize size=0;
  bool created=createD16DumbBuffer(3,1920,1080,&layout,&size,&fd);
  if(scenario>=1&&scenario<=4){assert(!created&&fd==-1&&owned.empty());assert(destroyCount==(scenario==1?0:1));}
  else{
   assert(created&&!gem&&destroyCount==1&&owned.count(fd)&&layout.offset==0&&layout.rowPitch==7680&&layout.size==8294400&&size==8294400);
   VkMemoryRequirements req={};req.size=8294400;req.alignment=4096;req.memoryTypeBits=4;VkDeviceMemory memory=VK_NULL_HANDLE;
   bool imported=importD16DumbMemory((VkImage)1,req,VK_MEMORY_PROPERTY_DEVICE_LOCAL_BIT,fd,size,&memory);
   assert(imported==(scenario==0));assert(memory==(scenario==0?(VkDeviceMemory)42:VK_NULL_HANDLE));
   assert(owned.size()==1&&owned.count(fd));fakeClose(fd);
  }
  assert(!gem&&owned.empty());
 }
}
'''
  with tempfile.TemporaryDirectory(prefix="rowanos-dumb-test-") as folder:
   folder=pathlib.Path(folder);neutral=folder/"include";neutral.mkdir()
   shutil.copytree(str(INCLUDE/"vulkan"),str(neutral/"vulkan"))
   if(INCLUDE/"vk_video").is_dir():shutil.copytree(str(INCLUDE/"vk_video"),str(neutral/"vk_video"))
   shutil.copytree(str(INCLUDE/"libdrm"),str(neutral/"libdrm"))
   shutil.copyfile(str(INCLUDE/"xf86drm.h"),str(neutral/"xf86drm.h"))
   cpp=folder/"test.cpp";cpp.write_text(harness);binary=folder/"test"
   subprocess.run(["g++","-std=c++17","-I"+str(neutral),"-I"+str(neutral/"libdrm"),str(cpp),"-o",str(binary)],check=True)
   subprocess.run([str(binary)],check=True)
if __name__=="__main__":unittest.main()
