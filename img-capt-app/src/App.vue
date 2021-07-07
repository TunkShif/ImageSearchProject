<template>
<div class="flex">
  <SideBar />
  <div class="flex p-5">
    <Folder path="/home/TunkShif/Downloads/Folder"/>
    <Folder path="/home/TunkShif/Downloads/TMP"/>
  </div>
</div>
</template>

<script>
import SideBar from './components/SideBar.vue'
import Folder from './components/Folder.vue'

export default {
  name: 'App',
  components: {
    SideBar,
    Folder
  }
}
</script>

<style>
</style>
