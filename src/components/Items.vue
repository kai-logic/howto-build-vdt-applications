<template>
  <div class="items-list">
    <div class="header">
      <h1>Items</h1>
    </div>
    <VdtGrid
      :assets="assets"
      :title="'metadata.filename'"
      :item-min-size="'10em'"
      :item-max-size="'1fr'"
      @assetClick="$emit('selected', $event)"/>
  </div>
</template>

<script>
// eslint-disable-next-line
import { VdtGrid } from '@vidispine/vdt-vue-components/es';
import itemApi from '../api/item.api';

export default {
  name: 'Items',
  components: {
    VdtGrid,
  },
  data() {
    return {
      assets: [],
    };
  },
  mounted() {
    return itemApi.getItems('', 1, 100).then((response) => {
      if (response.items.length) {
        this.assets = response.items;
      }
    });
  },
};
</script>

<style lang="scss">
.items-list {
  width: 100%;
  height: 100vh;
  overflow: auto;
  box-shadow: 1px 0 1px 10px #000;
  .vdt-grid-item {
    background: #3a539b;
    color: #f1f1f1;
  }
}
</style>

