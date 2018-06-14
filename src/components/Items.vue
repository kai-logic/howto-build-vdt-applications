<template>
  <div class="items-list">
    <h1>Items</h1>
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

<style lang="scss" scoped>
.items-list {
  width: 100%;
  height: 100vh;
}
</style>

