#!/usr/bin/env python3
"""Compile the real linear DMA-BUF capability helper against controlled ICD results."""
import pathlib
import subprocess
import shutil
import sys
import tempfile
import unittest

SOURCE = pathlib.Path(sys.argv.pop(1))
INCLUDE = pathlib.Path(sys.argv.pop(1))

class LinearExportTest(unittest.TestCase):
    def test_exact_usage_export_extent_and_view_format_requirements(self):
        source = SOURCE.read_text()
        marker = "static bool supportsLinearDmaBuf("
        start = source.find(marker)
        self.assertNotEqual(start, -1, "No validated linear DMA-BUF export capability helper exists")
        body = source.index("{", start)
        nesting, end = 1, body + 1
        while nesting:
            nesting += (source[end] == "{") - (source[end] == "}")
            end += 1
        helper = source[start:end]
        harness = r'''
#include <vulkan/vulkan_core.h>
#include <utility>
#include <cassert>
template <typename T>
const T *pNextFind(const void *base, VkStructureType type) {
  auto p = reinterpret_cast<const VkBaseInStructure *>(base);
  while (p) { if (p->sType == type) return reinterpret_cast<const T *>(p); p = p->pNext; }
  return nullptr;
}
struct Log { template<class... T> void infof(const char *,T...){} } vk_log;
static int scenario;
static constexpr VkImageUsageFlags expectedUsage = VK_IMAGE_USAGE_STORAGE_BIT | VK_IMAGE_USAGE_SAMPLED_BIT | VK_IMAGE_USAGE_TRANSFER_SRC_BIT;
static VkResult query(VkPhysicalDevice, const VkPhysicalDeviceImageFormatInfo2 *info, VkImageFormatProperties2 *out) {
  const auto external = pNextFind<VkPhysicalDeviceExternalImageFormatInfo>(info, VK_STRUCTURE_TYPE_PHYSICAL_DEVICE_EXTERNAL_IMAGE_FORMAT_INFO);
  const auto views = pNextFind<VkImageFormatListCreateInfo>(info, VK_STRUCTURE_TYPE_IMAGE_FORMAT_LIST_CREATE_INFO);
  if (!external || external->handleType != VK_EXTERNAL_MEMORY_HANDLE_TYPE_DMA_BUF_BIT_EXT ||
      info->tiling != VK_IMAGE_TILING_LINEAR || info->usage != expectedUsage ||
      info->flags != VK_IMAGE_CREATE_MUTABLE_FORMAT_BIT ||
      !views || views->viewFormatCount != 2 || views->pViewFormats[1] != VK_FORMAT_B8G8R8A8_SRGB)
      return VK_ERROR_FORMAT_NOT_SUPPORTED;
  if (scenario == 1) return VK_ERROR_FORMAT_NOT_SUPPORTED;
  auto ext = reinterpret_cast<VkExternalImageFormatProperties *>(out->pNext);
  ext->externalMemoryProperties.externalMemoryFeatures = scenario == 2 ? VK_EXTERNAL_MEMORY_FEATURE_IMPORTABLE_BIT : scenario == 6 ? (VK_EXTERNAL_MEMORY_FEATURE_IMPORTABLE_BIT | VK_EXTERNAL_MEMORY_FEATURE_EXPORTABLE_BIT) : scenario == 7 ? 0 : VK_EXTERNAL_MEMORY_FEATURE_EXPORTABLE_BIT;
  ext->externalMemoryProperties.compatibleHandleTypes = scenario == 3 ? VK_EXTERNAL_MEMORY_HANDLE_TYPE_OPAQUE_FD_BIT : VK_EXTERNAL_MEMORY_HANDLE_TYPE_DMA_BUF_BIT_EXT;
  out->imageFormatProperties.maxExtent = {scenario == 4 ? 1024u : 4096u, 4096u, 1u};
  out->imageFormatProperties.maxArrayLayers = 1;
  out->imageFormatProperties.maxMipLevels = 1;
  out->imageFormatProperties.sampleCounts = scenario == 5 ? VK_SAMPLE_COUNT_4_BIT : VK_SAMPLE_COUNT_1_BIT;
  return VK_SUCCESS;
}
struct Device {
  struct Dispatch { decltype(&query) GetPhysicalDeviceImageFormatProperties2 = query; } vk;
  VkPhysicalDevice physDev() { return VK_NULL_HANDLE; }
} g_device;
'''
        harness += helper
        harness += r'''
int main() {
  VkFormat formats[] = {VK_FORMAT_B8G8R8A8_UNORM, VK_FORMAT_B8G8R8A8_SRGB};
  VkImageFormatListCreateInfo views = {};
  views.sType = VK_STRUCTURE_TYPE_IMAGE_FORMAT_LIST_CREATE_INFO;
  views.viewFormatCount = 2; views.pViewFormats = formats;
  VkImageCreateInfo image = {};
  image.sType = VK_STRUCTURE_TYPE_IMAGE_CREATE_INFO; image.pNext = &views;
  image.imageType = VK_IMAGE_TYPE_2D; image.format = formats[0]; image.extent = {1920,1080,1};
  image.mipLevels = 1; image.arrayLayers = 1; image.samples = VK_SAMPLE_COUNT_1_BIT;
  image.flags = VK_IMAGE_CREATE_MUTABLE_FORMAT_BIT; image.usage = expectedUsage;
  scenario = 0; assert(supportsLinearDmaBuf(image,VK_EXTERNAL_MEMORY_FEATURE_EXPORTABLE_BIT));
  assert(!supportsLinearDmaBuf(image,VK_EXTERNAL_MEMORY_FEATURE_IMPORTABLE_BIT));
  for (scenario = 1; scenario <= 5; ++scenario) assert(!supportsLinearDmaBuf(image,VK_EXTERNAL_MEMORY_FEATURE_EXPORTABLE_BIT));
  scenario = 2; assert(supportsLinearDmaBuf(image,VK_EXTERNAL_MEMORY_FEATURE_IMPORTABLE_BIT));
  scenario = 6; assert(supportsLinearDmaBuf(image,VK_EXTERNAL_MEMORY_FEATURE_IMPORTABLE_BIT | VK_EXTERNAL_MEMORY_FEATURE_EXPORTABLE_BIT));
  scenario = 7; assert(!supportsLinearDmaBuf(image,VK_EXTERNAL_MEMORY_FEATURE_IMPORTABLE_BIT));
}
'''
        with tempfile.TemporaryDirectory(prefix="rowanos-linear-test-") as folder:
            cpp, binary = pathlib.Path(folder)/"test.cpp", pathlib.Path(folder)/"test"
            cpp.write_text(harness)
            # Vulkan headers are architecture-neutral; never use target glibc
            # headers while compiling this native capability-policy test.
            neutral = pathlib.Path(folder)/"include"
            neutral.mkdir()
            shutil.copytree(str(INCLUDE/"vulkan"), str(neutral/"vulkan"))
            if (INCLUDE/"vk_video").is_dir():
                shutil.copytree(str(INCLUDE/"vk_video"), str(neutral/"vk_video"))
            subprocess.run(["g++", "-std=c++17", "-I"+str(neutral), str(cpp), "-o", str(binary)], check=True)
            subprocess.run([str(binary)], check=True)

if __name__ == "__main__":
    unittest.main()
