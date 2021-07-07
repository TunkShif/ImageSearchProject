<template>
  <div class="flex flex-col items-center px-2">
    <a href="#" class="text-gray-600 hover:text-gray-400 text-8xl">
      <i class="fas fa-folder"></i>
    </a>
    <p class="font-medium text-gray-900 ">{{folderName}}</p>
  </div>
</template>

<script>
export default {
  name: "Folder",
  props: {
    path: String
  },
  computed: {
    folderName: function() {
      return this.path.split("/").pop()
    }
  }
}
</script>

<style>

</style>