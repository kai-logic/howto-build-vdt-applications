<template>
  <div class="version">
    <img src="../assets/images/VidispineDeveloperToolkitLogo.png" >'
    <h1>Vue + Django up and running! &#x1f44d; </h1>
    <p>Vidispine {{ VidispineVersion }}</p>
  </div>
</template>

<script>
import versionApi from '../api/version.api';

export default {
  name: 'VidispineVersion',
  data() {
    return {
      VidispineVersion: 'Error',
    };
  },
  mounted() {
    versionApi.getVersion().then((version) => {
      this.VidispineVersion = version.data.component[0].version;
    });
  },
};

</script>

<style lang="scss" scoped>
.version{
  text-align: center;

  img{
    padding-bottom: 2rem;
  }

  h1{
    font-size: 3rem;
  }

  p{
    font-size: 1.8rem;
  }
}
</style>
