<template>
  <div id="operation-plan-info">
    <!-- 情報 -->
    <div class="x_panel">
      <div class="x_title">
        <h2>運行計画 - 基本情報<small>運行計画を識別する名称などを設定します</small></h2>
        <div class="clearfix"></div>
      </div>
      <form role="form" data-toggle="validator">
        <div class="x_content" role="form" data-toggle="validator">
          <!-- 基本情報(1) -->
          <div class="col-md-7 form-horizontal form-label-left">

            <!-- name -->
            <div class="form-group">
              <label class="control-label col-md-2" for="name">名称 <span class="required">*</span></label>
              <div class="col-md-10">
                <input
                  type="text"
                  id="name"
                  required="required"
                  class="form-control"
                  v-model="planInfo.name"
                  @input="changeValue"
                >
              </div>
            </div>

            <!-- 車両 -->
            <div class="form-group">
              <label class="control-label col-md-2" for="vehicle">車両 <span class="required">*</span></label>
              <div class="col-md-10">
                <select id="vehicle" class="form-control" @change="changeValue" v-model="planInfo.vehicle">
                  <option v-for="v in vehicles" :value="v.id">
                    {{ v.name }}
                  </option>
                </select>
              </div>
            </div>

            <!-- 説明 -->
            <div class="form-group">
              <label class="control-label col-md-2" for="explain">説明</label>
              <div class="col-md-10">
                <textarea
                  name="explain"
                  id="explain"
                  rows="2"
                  class="form-control"
                  required="required"
                  v-model="planInfo.explain"
                  @input="changeValue"
                ></textarea>
              </div>
            </div>
          </div>

          <!-- 基本情報(2) -->
          <div class="col-md-5 form-horizontal form-label-left">

            <!-- 優先度 -->
            <div class="form-group">
              <label class="control-label col-md-4" for="priority">優先度 <span class="required">*</span></label>
              <div class="col-md-8">
                <input
                  type="text"
                  id="priority"
                  required="required"
                  class="form-control"
                  style="width:75px;"
                  v-model="planInfo.priority"
                  @input="changeValue"
                >
                <small>0が標準。数値が高いほど優先度が高くなる<br/>車両交差時に優先度に応じて走行する</small>
              </div>
            </div>

            <!-- PLC連携 -->
            <div class="form-group">
              <label class="control-label col-md-4" for="plc_signal_recv">PLC連携：受信後実行</label>
              <div class="col-md-8">
                <select id="plc_signal_recv" class="form-control">
                  <option>指定なし</option>
                  <option>A1:製品Aの製造が完了した</option>
                  <option>B1:製品B製造が完了した</option>
                </select>
                <small>運行開始のトリガーとなるPLC信号</small>
              </div>
              <label class="control-label col-md-4" for="plc_signal_send">PLC連携：完了時送信</label>
              <div class="col-md-8">
                <select id="plc_signal_send" class="form-control">
                  <option>指定なし</option>
                  <option>CMP1:製品Aの棚への移動が完了した</option>
                </select>
                <small>運行完了後に送信するPLC信号</small>
              </div>
            </div>

          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import * as Constants from './Constants'

export default {
  name: 'operation-plan-info',

  props: [
    'planInfo',
    'vehicles',
  ],

  data() {
    return {}
  },

  methods: {
    changeValue() {
      this.$emit('update:planInfo', this.planInfo);
    }
  },
}
</script>

<style scoped>
</style>
