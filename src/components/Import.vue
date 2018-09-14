<template>
  <div class="import">
    <div class="header">
      <h1>Import</h1>
      <select
        v-model="selectedStorage">
        <option
          disabled
          value="">
          Select a storage
        </option>
        <option
          v-for="storage in storages"
          :key="storage.id"
          :value="storage.id">
          {{ storage.name }}
        </option>
      </select>
    </div>
    <VdtList
      :assets="files"
      :columns="columns"
      :checkbox="true"
      :track-by="'id'"
      :selected-assets="selectedAssets"
      :break-point-width="0"/>
    <b-btn
      :disabled="selectedAssets.length < 1"
      variant="light"
      @click="importFiles()">
      Import
    </b-btn>
  </div>
</template>

<script>
import axios from 'axios';
// eslint-disable-next-line
import { VdtList } from '@vidispine/vdt-vue-components/es';
import storageApi from '../api/storage.api';
import fileApi from '../api/file.api';
import JobPollService from '../resources/JobPollService';

export default {
  name: 'Import',
  components: {
    VdtList,
  },
  data() {
    return {
      storages: [],
      files: [],
      selectedStorage: '',
      selectedAssets: [],
      intervals: [],
      columns: [
        {
          label: 'Path',
          key: 'path',
          type: 'String',
          size: 'large',
        },
        {
          label: 'Date',
          key: 'timestamp',
          type: 'Date',
          size: 'medium',
        },
        {
          label: 'Size',
          key: 'size',
          type: 'Size',
          size: 'small',
        },
      ],
    };
  },
  watch: {
    selectedStorage(newStorage) {
      this.getFiles(newStorage);
    },
  },
  mounted() {
    storageApi.getStorages().then((response) => {
      this.storages = response;
    });
  },
  destroyed() {
    this.intervals.forEach((interval) => {
      interval.stopInterval();
    });
  },
  methods: {
    getFiles(storageId) {
      return fileApi.getImportableFiles(storageId).then((response) => {
        this.files = response.files.files;
      });
    },
    importFiles() {
      this.selectedAssets.forEach((file) => {
        const data = {/* insert custom data here, tags etc. */};
        const fileExtention = file.path.substr(file.path.lastIndexOf('.') + 1);
        if (['png', 'jpg', 'JPG', 'jpeg', 'gif', 'webp', 'tiff', 'bmp'].indexOf(fileExtention) > -1) {
          data.tag = '__jpeg';
        } else if (['mp4', 'mov', 'avi', 'mkv', 'flv', 'webm', 'wmv', 'mpeg', 'mpg', 'mpv', 'm4v', 'mxf'].indexOf(fileExtention) > -1) {
          data.tag = '__mp4';
        }
        axios.post(`/api/storage/${this.selectedStorage}/file/${file.id}/import`, data)
          .then((response) => {
            const job = new JobPollService({
              jobId: response.data.jobId,
              milliseconds: 2000,
              asset: file,
            });
            job.startInterval();
            this.intervals.push(job);
          });
      });
    },
  },
};
</script>

<style lang="scss">
.import {
  position: relative;
  width: 100%;
  height: 100vh;
  overflow: auto;
  background: #2a2a2a;
  select {
    width: 100%;
  }
  button {
    margin: 1em 0 0 1em;
  }
}
.vdt-list-row {
  letter-spacing: -.5px;
}
.vdt-list__header--column {
  color: #fff !important;
}
.vdt-list-row__selected{
  background-color: #5a5a5a;
}
.vdt-bulk-boolean--checked {
  color: #fff !important;
  fill: #fff !important;
}
</style>

