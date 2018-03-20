<template>
  <div id="operation-plan-info">
    <!-- 情報 -->
    <div class="x_panel">
      <div class="x_title">
        <h2>運行計画 - 基本情報<small>運行計画を識別する名称などを設定します</small></h2>
        <div class="clearfix"></div>
      </div>

      <div class="x_content">
        <!-- 基本情報(1) -->
        <div class="col-md-7 form-horizontal form-label-left">

          <!-- name -->
          <div class="form-group">
            <label class="control-label col-md-2" for="name">名称 <span class="required">*</span></label>
            <div class="col-md-10">
              <input type="text" id="name" required="required" class="form-control"
                     :value="this.planInfo.name" @input="changeValue">
            </div>
          </div>

          <!-- 車両 -->
          <div class="form-group">
            <label class="control-label col-md-2" for="vehicle">車両 <span class="required">*</span></label>
            <div class="col-md-10">
              <select id="vehicle" class="form-control" @change="changeValue">
                <option v-for="v in this.planInfo.vehicles" v-bind:value="v.id">
                  {{ v.name }}
                </option>
              </select>
            </div>
          </div>

          <!-- 説明 -->
          <div class="form-group">
            <label class="control-label col-md-2" for="explain">説明</label>
            <div class="col-md-10">
              <textarea name="explain" id="explain" rows="2" class="form-control"
                        :value="this.planInfo.explain" @input="changeValue"></textarea>
            </div>
          </div>
        </div>

        <!-- 基本情報(2) -->
        <div class="col-md-5 form-horizontal form-label-left">

          <!-- 優先度 -->
          <div class="form-group">
            <label class="control-label col-md-4" for="priority">優先度 <span class="required">*</span></label>
            <div class="col-md-8">
              <input type="text" id="priority" required="required" class="form-control" style="width:75px;"
                     :value="this.planInfo.priority" @input="changeValue">
              <small>0が標準。数値が高いほど優先度が高くなる<br/>車両交差時に優先度に応じて走行する</small>
            </div>
          </div>

          <!-- PLC連携 -->
          <div class="form-group">
            <label class="control-label col-md-4" for="plc_signal">PLC信号連携</label>
            <div class="col-md-8">
              <select id="plc_signal" class="form-control">
                <option>指定なし</option>
              </select>
              <small>運行開始のトリガーとなるPLC信号</small>
            </div>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script>
import * as Constants from './Constants'

export default {
  name: 'operation-plan-info',

  props: [
    'planInfo',
  ],

  data() {
    return {}
  },

  methods: {
    changeValue(event) {
      let ret = {}
      ret[event.target.id] = event.target.value;
      this.$emit('changeValue', ret);
    }
  },
}
</script>

<style scoped>
</style>
