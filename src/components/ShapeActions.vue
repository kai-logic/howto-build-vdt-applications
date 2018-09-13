<template>
  <div class="buttons">
    <b-btn
      v-b-modal.TranscodeModal
      size="md"
      variant="dark">
      Transcode
    </b-btn>
    <b-btn
      v-b-modal.QcModal
      variant="dark"
      size="md">
      Quality Control
    </b-btn>
    <b-btn
      v-b-modal.ExportModal
      variant="dark"
      size="md">
      Export
    </b-btn>
    <b-modal
      id="TranscodeModal"
      title="Transcode"
      button-size="md"
      lazy>
      <VdtTranscode
        :item-id="item.metadata.id"
        :filename="item.metadata.filename"
        :tags="tags"
        :cost-estimate-url="transcodeUrl"
        :start-transcode-url="transcodeUrl"
        :job-status-url="jobUrl"
        :abort-job-url="jobUrl"
        :poll-interval="4000"/>
    </b-modal>
    <b-modal
      id="QcModal"
      title="Quality Control"
      button-size="md"
      lazy>
      <VdtVidinetQC
        :item-id="item.metadata.id"
        :shape-id="shape.id"
        :shape-tag="shape.tag"
        :resources="resources"
        :cost-estimate-url="qcUrl"
        :start-qc-url="qcUrl"
        :job-status-url="jobUrl"
        :abort-job-url="jobUrl"
        :poll-interval="4000"/>
    </b-modal>
    <b-modal
      id="ExportModal"
      title="Export"
      button-size="md"
      lazy>
      <VdtShapeExport
        :item-id="item.metadata.id"
        :shape-id="shape.id"
        :tag="shape.tag"
        :export-location-url="exportLocationUrl"
        :start-export-url="startExportUrl"
        :job-status-url="jobUrl"
        :poll-interval="4000"/>
    </b-modal>
  </div>
</template>

<script>
import axios from 'axios';
// eslint-disable-next-line
import { VdtTranscode, VdtVidinetQC, VdtShapeExport } from '@vidispine/vdt-vue-components/es';
import shapeApi from '../api/shape.api';

export default {
  name: 'ShapeActions',
  components: {
    VdtTranscode,
    VdtVidinetQC,
    VdtShapeExport,
  },
  props: {
    item: {
      type: Object,
      required: true,
    },
    shape: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      transcodeUrl: '/api/transcode',
      qcUrl: '/api/vidinet/qc',
      exportLocationUrl: '/api/export-location',
      startExportUrl: '/api/shape-export',
      jobUrl: '/api/job/',
      tags: [],
      resources: [],
    };
  },
  watch: {
    shape() {
      shapeApi.getShapeTags(this.shape.id).then((response) => {
        this.tags = response;
      });
    },
  },
  mounted() {
    shapeApi.getShapeTags(this.shape.id).then((response) => {
      this.tags = response;
    });
    axios.get('/api/resource?resourceType=vidinet').then((response) => {
      this.resources = response.data.resource;
    });
  },
};
</script>

<style lang="scss" scoped>
.buttons {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  grid-column-gap: 1em;
}
</style>
