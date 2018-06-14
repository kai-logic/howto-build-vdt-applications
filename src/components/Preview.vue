<template>
  <div class="preview">
    <div v-if="item.metadata">
      <div class="preview-item">
        <h1>{{ `${item.metadata.filename} (${item.metadata.id})` }}</h1>
        <select
          v-model="selectedShape">
          <option
            disabled
            value="">
            Select a shape
          </option>
          <option
            v-for="shape in item.shapes"
            :key="shape.id"
            :value="shape">
            {{ shape.tag }}
          </option>
        </select>
        <div v-if="selectedShape">
          <VdtImagePreview
            v-if="itemType === 'image'"
            :shape="selectedShape"/>
          <VdtVideoPlayer
            v-if="itemType === 'video'"
            :shape="selectedShape"/>
          <VdtMetadata
            :asset="item"
            :rows="rows"/>
        </div>
      </div>
      <div class="preview-metadata">
        <VdtShape
          v-for="shape in item.shapes"
          :key="shape.id"
          :shape="shape"
          :item="item"/>
      </div>
    </div>
  </div>
</template>

<script>
// eslint-disable-next-line
import { VdtShape, VdtMetadata, VdtImagePreview, VdtVideoPlayer } from '@vidispine/vdt-vue-components/es';
import itemApi from '../api/item.api';

export default {
  name: 'Preview',
  components: {
    VdtShape,
    VdtMetadata,
    VdtImagePreview,
    VdtVideoPlayer,
  },
  props: {
    itemId: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      item: {},
      selectedShape: '',
      rows: [
        {
          label: 'Title',
          key: 'metadata.filename',
          type: 'String',
        },
        {
          label: 'Type',
          key: 'metadata.mediaType',
          type: 'String',
        },
        {
          label: 'Format',
          key: 'metadata.originalFormat',
          type: 'String',
        },
        {
          label: 'Created',
          key: 'metadata.created',
          type: 'Date',
        },
      ],
    };
  },
  computed: {
    itemType() {
      return this.item.metadata.mediaType;
    },
  },
  watch: {
    itemId(newVal, oldVal) {
      if (oldVal === null || newVal !== oldVal) {
        itemApi.getItem(this.itemId).then((response) => {
          this.item = response;
          [this.selectedShape] = [response.shapes[0]];
        });
      }
    },
  },
};
</script>

<style lang="scss" scoped>
.preview {
  width: 100%;
  height: 100vh;
  overflow: auto;
}
</style>
