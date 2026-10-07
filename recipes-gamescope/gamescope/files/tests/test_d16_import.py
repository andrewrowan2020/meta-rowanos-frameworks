#!/usr/bin/env python3
"""Exercise actual D16 DMA heap import and layout guards with controlled APIs."""
import pathlib, shutil, subprocess, sys, tempfile, unittest
SOURCE = pathlib.Path(sys.argv.pop(1))
INCLUDE = pathlib.Path(sys.argv.pop(1))
def extract(source, marker):
    start = source.find(marker)
    if start < 0: raise AssertionError("Missing production helper: "+marker)
    body = source.index("{", start); end = body+1; depth = 1
    while depth:
        depth += (source[end]=="{") - (source[end]=="}"); end += 1
    return source[start:end] + (";" if marker.startswith("class ") else "")
class D16ImportTest(unittest.TestCase):
    def test_import_fd_ownership_intersection_and_layout_bounds(self):
        source = SOURCE.read_text()
        helpers = "\n".join(extract(source, marker) for marker in (
            "class D16ScopedFd", "static bool allocateD16ScanoutMemory(", "static bool validD16LinearLayout("))
        harness = r'''
#include <vulkan/vulkan_core.h>
#include <linux/dma-heap.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <utility>
#include <cassert>
#include <cstdint>
#include <climits>
#include <set>
#include <cstring>
static int scenario, nextFd;
static std::set<int> owned;
static int fakeOpen(const char *path, int flags) {
 assert(!strcmp(path,"/dev/dma_heap/system") && (flags & O_CLOEXEC));
 if(scenario==1) return -1; owned.insert(++nextFd); return nextFd;
}
static int fakeClose(int fd) { assert(owned.erase(fd)==1); return 0; }
static int fakeFcntl(int fd, int cmd, int) {
 assert(owned.count(fd) && cmd==F_DUPFD_CLOEXEC);
 if(scenario==5) return -1; owned.insert(++nextFd); return nextFd;
}
static int fakeIoctl(int fd, unsigned long request, dma_heap_allocation_data *data) {
 assert(owned.count(fd) && request==DMA_HEAP_IOCTL_ALLOC && data->len==8192);
 assert(data->fd_flags==(O_RDWR|O_CLOEXEC));
 if(scenario==2) return -1;
 owned.insert(++nextFd); data->fd=nextFd; return 0;
}
static off_t fakeLseek(int fd, off_t, int whence) {
 assert(owned.count(fd) && whence==SEEK_END);
 return scenario==7 ? 4096 : scenario==8 ? -1 : 8192;
}
#define open fakeOpen
#define close fakeClose
#define fcntl fakeFcntl
#define ioctl fakeIoctl
#define lseek fakeLseek
static VkResult fdProps(VkDevice, VkExternalMemoryHandleTypeFlagBits type, int fd, VkMemoryFdPropertiesKHR *out) {
 assert(type==VK_EXTERNAL_MEMORY_HANDLE_TYPE_DMA_BUF_BIT_EXT && owned.count(fd));
 if(scenario==3) return VK_ERROR_INVALID_EXTERNAL_HANDLE;
 out->memoryTypeBits=scenario==4 ? 2 : 5; return VK_SUCCESS;
}
static VkResult allocate(VkDevice, const VkMemoryAllocateInfo *info, const VkAllocationCallbacks *, VkDeviceMemory *memory) {
 assert(info->allocationSize==8192 && info->memoryTypeIndex==2);
 const auto *import = reinterpret_cast<const VkImportMemoryFdInfoKHR *>(info->pNext);
 assert(import->sType==VK_STRUCTURE_TYPE_IMPORT_MEMORY_FD_INFO_KHR && import->handleType==VK_EXTERNAL_MEMORY_HANDLE_TYPE_DMA_BUF_BIT_EXT);
 const auto *dedicated = reinterpret_cast<const VkMemoryDedicatedAllocateInfo *>(import->pNext);
 assert(dedicated->sType==VK_STRUCTURE_TYPE_MEMORY_DEDICATED_ALLOCATE_INFO && dedicated->image!=(VkImage)0 && !dedicated->pNext);
 if(scenario==6) return VK_ERROR_OUT_OF_DEVICE_MEMORY;
 assert(owned.erase(import->fd)==1); *memory=(VkDeviceMemory)42; return VK_SUCCESS;
}
struct Device {
 struct Dispatch { decltype(&fdProps) GetMemoryFdPropertiesKHR=fdProps; decltype(&allocate) AllocateMemory=allocate; } vk;
 VkDevice device() { return VK_NULL_HANDLE; }
 int32_t findMemoryType(VkMemoryPropertyFlags props, uint32_t bits) {
  if(scenario==9 && props) return -1;
  return bits & 4 ? 2 : -1;
 }
} g_device;
struct Log { template<class... T> void errorf(const char *,T...){} template<class... T> void errorf_errno(const char *,T...){} } vk_log;
static void vk_errorf(VkResult,const char *){}
'''
        harness += helpers
        harness += r'''
int main() {
 VkMemoryRequirements req={}; req.size=8192; req.alignment=4096; req.memoryTypeBits=4;
 for(scenario=0;scenario<=9;scenario++){
  nextFd=10; owned.clear(); VkDeviceMemory memory=VK_NULL_HANDLE; int backing=-1;
  bool ok=allocateD16ScanoutMemory((VkImage)1,req,VK_MEMORY_PROPERTY_DEVICE_LOCAL_BIT,&memory,&backing);
  if(scenario==0 || scenario==9) {
   assert(ok && memory==(VkDeviceMemory)42 && owned.size()==1 && owned.count(backing)); fakeClose(backing);
  } else assert(!ok && backing==-1 && memory==VK_NULL_HANDLE);
  assert(owned.empty());
 }
 VkSubresourceLayout layout={}; layout.rowPitch=7680; layout.offset=0; layout.size=8294400;
 assert(validD16LinearLayout(layout,1920,1080,8294400));
 layout.rowPitch=7679; assert(!validD16LinearLayout(layout,1920,1080,8294400));
 layout.rowPitch=7680; layout.offset=4096; assert(!validD16LinearLayout(layout,1920,1080,8294400));
 assert(validD16LinearLayout(layout,1920,1080,8298496));
 layout.offset=UINT64_MAX; assert(!validD16LinearLayout(layout,1920,1080,UINT64_MAX));
 layout.offset=0; layout.rowPitch=UINT64_MAX; assert(!validD16LinearLayout(layout,1920,1080,UINT64_MAX));
 layout.rowPitch=7680; assert(!validD16LinearLayout(layout,1920,0,8294400));
}
'''
        with tempfile.TemporaryDirectory(prefix="rowanos-import-test-") as folder:
            folder=pathlib.Path(folder); neutral=folder/"include"; neutral.mkdir()
            shutil.copytree(str(INCLUDE/"vulkan"),str(neutral/"vulkan"))
            (neutral/"linux").mkdir()
            shutil.copyfile(str(INCLUDE/"linux/dma-heap.h"),str(neutral/"linux/dma-heap.h"))
            if (INCLUDE/"vk_video").is_dir(): shutil.copytree(str(INCLUDE/"vk_video"),str(neutral/"vk_video"))
            cpp=folder/"test.cpp"; cpp.write_text(harness); binary=folder/"test"
            subprocess.run(["g++","-std=c++17","-I"+str(neutral),str(cpp),"-o",str(binary)],check=True)
            subprocess.run([str(binary)],check=True)
if __name__=="__main__": unittest.main()
