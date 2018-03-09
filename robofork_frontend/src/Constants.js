export const OPERATION_ENDPOINT = '/static/robofork_app/api/operation_control.json';
export const START_ID = 0;

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

// マップモード
export const MODE_ROUTING = 0;
export const MODE_POINT_EDIT = 1;

// 次の進行方向のラベル
export const DIR_FORWARD = '前進方向';
export const DIR_REVERSE = 'バック方向';
