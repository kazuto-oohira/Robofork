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
              <input type="text" id="name" required="required" class="form-control">
            </div>
          </div>

          <!-- 車両 -->
          <div class="form-group">
            <label class="control-label col-md-2" for="vehicle">車両 <span class="required">*</span></label>
            <div class="col-md-10">
              <select id="vehicle" class="form-control">
                <option>3号機</option>
                <option>1号機</option>
              </select>
            </div>
          </div>

          <!-- 説明 -->
          <div class="form-group">
            <label class="control-label col-md-2" for="explain">説明</label>
            <div class="col-md-10">
              <textarea name="explain" id="explain" rows="2" class="form-control"></textarea>
            </div>
          </div>
        </div>

        <!-- 基本情報(2) -->
        <div class="col-md-5 form-horizontal form-label-left">

          <!-- 優先度 -->
          <div class="form-group">
            <label class="control-label col-md-4" for="priority">優先度 <span class="required">*</span></label>
            <div class="col-md-8">
              <input type="text" id="priority" required="required" class="form-control" value="0" style="width:75px;">
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
    // 'hasCommands',
    // 'animate',
    // 'currentDir',
  ],

  data() {
    return {
    }
  },

  computed: {
    // dirLabel() {
    //   if (!this.hasCommands) {
    //     return '-';
    //   }
    //
    //   return this.currentDir ? Constants.DIR_FORWARD : Constants.DIR_REVERSE;
    // },
  },

  methods: {
    // reverse() {
    //   this.$emit('reverse');
    // },
    //
    // save() {
    //   this.$emit('save');
    // },
  },
}
</script>

<style scoped>
/*.checkbox label {*/
  /*user-select: none;*/
/*}*/

/*.row {*/
  /*margin-bottom: 1rem;*/
/*}*/
</style>
