<template>
  <v-app>
      <v-app-bar
          app
          dark
      >
        <a href="/">
          <v-img
              :src="require('./assets/nginx.png')"
              contain
              height="50"
              width="50">
          </v-img>
        </a>
        <v-toolbar-title>Nginx UI</v-toolbar-title>
      </v-app-bar>
      <v-main>
        <v-container fluid>
          <router-view/>
        </v-container>
      </v-main>
      <v-footer app></v-footer>
  </v-app>
</template>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>
