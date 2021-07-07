<template>
  <div class="flex flex-col items-center justify-start h-screen p-2 text-3xl text-gray-700 bg-gray-200 shadow-md ">
    <a href="#" class="hover:text-gray-500">
      <i class="fas fa-bars"></i>
    </a>
    <a href="#" @click="modelInit" class="hover:text-gray-500">
      <i class="fas fa-home"></i>
    </a>
    <a href="#" @click="addFolder" class="hover:text-gray-500">
      <i class="fas fa-plus"></i>
    </a>
  </div>
</template>

<script>
import {ipcRenderer} from 'electron'

export default {
  name: "SideBar",
  methods: {
    modelInit: function() {
      fetch('http://localhost:8000/model_init')
       .then(response => response.json())
       .then(data => console.log(data))
    },
    addFolder: function() {
      ipcRenderer.send('openFolder')
      ipcRenderer.on('filePaths', (event, filePaths) => {
        if (filePaths.length != 0) {
          fetch('http://localhost:8000/folders', {
            method: 'POST',
            body: new URLSearchParams('path=' + filePaths[0])
          }).then(response => response.json()).then(data => console.log(data))
        }
      })
    }
  }
}
</script>

<style scoped>

</style>