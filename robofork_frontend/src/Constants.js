// API など
export const CONFIG_ENDPOINT = (id) => `/api/operation_plan/${id}/config`;
export const LOAD_ENDPOINT = (id) => `/api/operation_plan/${id}/load`;
export const SAVE_ENDPOINT = (id) => `/api/operation_plan/${id}/save`;
export const VEHICLES_ENDPOINT = '/api/vehicle_operation_status/load';

// HOME 画面での車両ポップアップの色ごとの追加クラス名
export const STATUS_CODE_CLASSNAMES = {
  0: '',
  1: 'my-warning',
  2: 'my-danger',
};

// command の連番
export const START_NODE_INDEX = 0;

// タスク定義
export const TASK_FORWARD            = 0;
export const TASK_REVERSE            = 1;
export const TASK_TURN               = 2;
export const TASK_LIFTUP             = 3;
export const TASK_LIFTUP_WITH_TURN   = 4;
export const TASK_LIFTDOWN           = 5;
export const TASK_LIFTDOWN_WITH_TURN = 6;
export const TASK_NOTHING            = 255;

// タスクラベル
export const TASK_LABELS = {
  [TASK_FORWARD]:            '前進',
  [TASK_REVERSE]:            'バック',
  [TASK_TURN]:               '旋回（回転）',
  [TASK_LIFTUP]:             '荷上げ',
  [TASK_LIFTUP_WITH_TURN]:   '荷上げ(旋回あり)',
  [TASK_LIFTDOWN]:           '荷下げ',
  [TASK_LIFTDOWN_WITH_TURN]: '荷下げ(旋回あり)',
  [TASK_NOTHING]:            'なにもしない',
};

// タスク: Speed の初期値
export const INITIAL_SPEED = 1000;

// タスク: Angle の初期値
export const INITIAL_ANGLE = 0;

// マップモード
export const MODE_ROUTING = 0;
export const MODE_POINT_EDIT = 1;

// マップ上でのアニメーションスピード（サブノード1つ分、ミリ秒）
export const ANIMATION_SPEED = 100;

// 次の進行方向のラベル
export const DIR_FORWARD = '前進方向';
export const DIR_REVERSE = 'バック方向';
