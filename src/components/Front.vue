<template>
  <div class="media-supply-chain-wrapper">
    <Import/>
    <Items @selected="select($event)"/>
    <Preview :item-id="itemId"/>
  </div>
</template>

<script>
import Import from './Import.vue';
import Items from './Items.vue';
import Preview from './Preview.vue';

export default {
  name: 'MediaSupplyChain',
  components: {
    Import,
    Items,
    Preview,
  },
  data() {
    return {
      itemId: '',
    };
  },
  methods: {
    select(asset) {
      this.itemId = asset.metadata.id;
    },
  },
};
</script>

<style lang="scss">
.media-supply-chain-wrapper {
  display: grid;
  grid-template-columns: 1fr 2fr 1fr;
  height: 100vh;
  overflow: auto;
  font-size: 1rem;
  background: #3a3a3a;
  > div {
    // padding: 1em;
    color: #fff;
  }
}
.header {
  padding: 0 .5em;
}
</style>
