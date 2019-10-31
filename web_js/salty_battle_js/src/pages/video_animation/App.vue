<template>
  <div>
      <!-- <center> -->
      <center style="width:100%; margin:0px; display: block">

        <div :style="'width:100%'">
            <div style="position:relative;width:100%;height:0;padding-bottom: 56.25%;overflow: hidden;">

              <div style="position:absolute; top:0; left:0; width:100%; height:100%; z-index:-50">
                <div style="height:30%"/>
                  <TextBigMessage style="width:100%" :label="bigMessageText" />
              </div>

              <!-- <div style="position:absolute; top:10%; left:20%; width:60%; height:30%; z-index:50;text-color:black">{{current_second}}</div> -->

              <div style="position:absolute; top:70%; left:40%; width:20%; height:10%; z-index:50">
                <PopBaloon :pose="bonusBaloonShow?'visible':'hidden'">
                  <BonusBaloon :symbol="bonusBaloonSymbol"/>
                </PopBaloon>
              </div>

              <div style="position: absolute;top:80%;left:10%;width:80%;height:5%;">
                <HpBar :left="left.score_pcnt" :right="right.score_pcnt"/>
              </div>

              <div style="position: absolute;top:80%;left:12%;width:78%; height:15%;">
                <div class="d-flex justify-content-between" style="height:100%;width:100%">
                  <div><ScoreIncrement style="height=100%;width:40%" :score="left.score_increment" ref="ref_score_incr_left"/></div>
                  <div><ScoreIncrement style="height=100%;width:40%;" :score="right.score_increment" ref="ref_score_incr_right"/></div>
                </div>
              </div>

              <div style="position: absolute;top:80%;left:0;width:100%; height:20%;">
                <div class="d-flex justify-content-between" style="height:100%;z-index:-10">
                  <!-- <div style="width:30%"> -->
                  <LuchaEmoji style="width:30%" :pose="leftLuchaPose">
                    <svg style="position:relative;display: inline-block;width:100%;height:100%;" viewBox="0 0 300 200">
                      <LuchoMucho :symbol="emojis[left.emoji]" width="150" x="40"/>
                      <TextVLabel x="-100" y="40" height="50" label="LEFT"/>
                    </svg>
                  </LuchaEmoji>
                  <!-- </div> -->
                  <!-- <div style="width:30%"> -->
                  <LuchaEmoji style="width:30%" :pose="rightLuchaPose">
                    <svg style="position:relative;display: inline-block;width:100%;height:100%;" viewBox="0 0 300 200">
                      <LuchaChili :symbol="emojis[right.emoji]" width="150" x="100"/>
                      <TextVLabel x="130" y="40" height="50" label="RIGHT"/>
                    </svg>
                  </LuchaEmoji>
                  <!-- </div> -->
                </div>
              </div>

            </div>
        </div>
      <!-- </center> -->
    </center>
  </div>
</template>

<script>
import FontAwesome from '../../components/FontAwesome.vue';
import LuchaChili from '../../components/LuchaChili.vue';
import LuchoMucho from '../../components/LuchoMucho.vue';
import BonusBaloon from '../../components/BonusBaloon.vue';
import HpBar from '../../components/HpBar.vue';
import ScoreIncrement from '../../components/ScoreIncrement.vue';
import TextVLabel from '../../components/TextVLabel.vue';
import TextBigMessage from '../../components/TextBigMessage.vue';
import posed, { PoseTransition } from "vue-pose";

let log_data = {
  start_offset: 467,
  messages: [
    // [469, "QUARTER FINALS"],
    [470, "battle_start"],
    // [470, "WARM UP"],
    // [482, "BATTLE START"],
    [482, {"left": {"total": 3, "increment": 3, "is_bonus": false, "bonus_message": ""}, "right": {"total": 0, "increment": 0, "is_bonus": false, "bonus_message": ""}}],
    [483, {"left": {"total": 4, "increment": 1, "is_bonus": false, "bonus_message": ""}, "right": {"total": 1, "increment": 1, "is_bonus": false, "bonus_message": ""}}],
    [484, {"left": {"total": 4, "increment": 0, "is_bonus": false, "bonus_message": ""}, "right": {"total": 1, "increment": 0, "is_bonus": false, "bonus_message": ""}}],
    [485, {"left": {"total": 4, "increment": 0, "is_bonus": false, "bonus_message": ""}, "right": {"total": 1, "increment": 0, "is_bonus": false, "bonus_message": ""}}],
    [487, {"left": {"total": 4, "increment": 0, "is_bonus": false, "bonus_message": ""}, "right": {"total": 1, "increment": 0, "is_bonus": false, "bonus_message": ""}}],
    [488, {"left": {"total": 5, "increment": 1, "is_bonus": false, "bonus_message": ""}, "right": {"total": 1, "increment": 0, "is_bonus": false, "bonus_message": ""}}],
    [488, "WARM UP"],
    [490, "BATTLE START"],
    [490, {"left_lucha_pose": "normal"}],
    [490, {"right_lucha_pose": "normal"}],
    [490, {"left": {"total": 6, "increment": 1, "is_bonus": false, "bonus_message": ""}, "right": {"total": 2, "increment": 1, "is_bonus": false, "bonus_message": ""}}],
    [490, {"left": {"total": 8, "increment": 2, "is_bonus": false, "bonus_message": ""}, "right": {"total": 3, "increment": 1, "is_bonus": false, "bonus_message": ""}}],
    [491, {"left": {"total": 9, "increment": 1, "is_bonus": false, "bonus_message": ""}, "right": {"total": 8, "increment": 5, "is_bonus": false, "bonus_message": ""}}],
    [492, {"left": {"total": 9, "increment": 0, "is_bonus": false, "bonus_message": ""}, "right": {"total": 20, "increment": 12, "is_bonus": false, "bonus_message": ""}}],
    [495, {"left": {"total": 21, "increment": 12, "is_bonus": false, "bonus_message": ""}, "right": {"total": 134, "increment": 114, "is_bonus": true, "bonus_message": "andale"}}],
    [496, {"left": {"total": 187, "increment": 166, "is_bonus": true, "bonus_message": "andale"}, "right": {"total": 275, "increment": 141, "is_bonus": true, "bonus_message": "andale"}}],
    [497, {"left": {"total": 316, "increment": 129, "is_bonus": true, "bonus_message": ""}, "right": {"total": 283, "increment": 8, "is_bonus": false, "bonus_message": ""}}],
    [499, {"left": {"total": 338, "increment": 22, "is_bonus": false, "bonus_message": ""}, "right": {"total": 294, "increment": 11, "is_bonus": false, "bonus_message": ""}}],
    [500, {"left": {"total": 531, "increment": 193, "is_bonus": true, "bonus_message": ""}, "right": {"total": 435, "increment": 141, "is_bonus": true, "bonus_message": "ay-caramba"}}],
    [501, {"left": {"total": 577, "increment": 46, "is_bonus": false, "bonus_message": ""}, "right": {"total": 461, "increment": 26, "is_bonus": false, "bonus_message": ""}}],
    [503, {"left": {"total": 629, "increment": 52, "is_bonus": false, "bonus_message": ""}, "right": {"total": 737, "increment": 276, "is_bonus": true, "bonus_message": "el-impacto"}}],
    [504, {"left": {"total": 656, "increment": 27, "is_bonus": false, "bonus_message": ""}, "right": {"total": 994, "increment": 257, "is_bonus": true, "bonus_message": "que-chulo"}}],
    [506, {"left": {"total": 686, "increment": 30, "is_bonus": false, "bonus_message": ""}, "right": {"total": 1037, "increment": 43, "is_bonus": false, "bonus_message": ""}}],
    [507, {"left": {"total": 1103, "increment": 417, "is_bonus": true, "bonus_message": ""}, "right": {"total": 1334, "increment": 297, "is_bonus": true, "bonus_message": "ay-caramba"}}],
    [508, {"left": {"total": 1148, "increment": 45, "is_bonus": false, "bonus_message": ""}, "right": {"total": 1369, "increment": 35, "is_bonus": false, "bonus_message": ""}}],
    [509, {"left": {"total": 1183, "increment": 35, "is_bonus": false, "bonus_message": ""}, "right": {"total": 1414, "increment": 45, "is_bonus": false, "bonus_message": ""}}],
    [511, {"left": {"total": 1229, "increment": 46, "is_bonus": false, "bonus_message": ""}, "right": {"total": 1456, "increment": 42, "is_bonus": false, "bonus_message": ""}}],
    [512, {"left": {"total": 1785, "increment": 556, "is_bonus": true, "bonus_message": "soy-la-leche"}, "right": {"total": 1501, "increment": 45, "is_bonus": false, "bonus_message": ""}}],
    [514, {"left": {"total": 1828, "increment": 43, "is_bonus": false, "bonus_message": ""}, "right": {"total": 1518, "increment": 17, "is_bonus": false, "bonus_message": ""}}],
    [514, {"left": {"total": 1861, "increment": 33, "is_bonus": false, "bonus_message": ""}, "right": {"total": 1539, "increment": 21, "is_bonus": false, "bonus_message": ""}}],
    [515, {"left": {"total": 2450, "increment": 589, "is_bonus": true, "bonus_message": "ay-caramba"}, "right": {"total": 1554, "increment": 15, "is_bonus": false, "bonus_message": ""}}],
    [517, {"left": {"total": 2507, "increment": 57, "is_bonus": false, "bonus_message": ""}, "right": {"total": 1570, "increment": 16, "is_bonus": false, "bonus_message": ""}}],
    [518, {"left": {"total": 3110, "increment": 603, "is_bonus": true, "bonus_message": "soy-la-leche"}, "right": {"total": 1610, "increment": 40, "is_bonus": false, "bonus_message": ""}}],
    [519, {"left": {"total": 3139, "increment": 29, "is_bonus": false, "bonus_message": ""}, "right": {"total": 1633, "increment": 23, "is_bonus": false, "bonus_message": ""}}],
    [520, {"left": {"total": 3154, "increment": 15, "is_bonus": false, "bonus_message": ""}, "right": {"total": 1653, "increment": 20, "is_bonus": false, "bonus_message": ""}}],
    [522, {"left": {"total": 3180, "increment": 26, "is_bonus": false, "bonus_message": ""}, "right": {"total": 1696, "increment": 43, "is_bonus": false, "bonus_message": ""}}],
    [523, {"left": {"total": 3219, "increment": 39, "is_bonus": false, "bonus_message": ""}, "right": {"total": 2836, "increment": 1140, "is_bonus": true, "bonus_message": "ay-caramba"}}],
    [524, {"left": {"total": 3248, "increment": 29, "is_bonus": false, "bonus_message": ""}, "right": {"total": 2892, "increment": 56, "is_bonus": false, "bonus_message": ""}}],
    [525, {"left": {"total": 3270, "increment": 22, "is_bonus": false, "bonus_message": ""}, "right": {"total": 2951, "increment": 59, "is_bonus": false, "bonus_message": ""}}],
    [527, {"left": {"total": 3298, "increment": 28, "is_bonus": false, "bonus_message": ""}, "right": {"total": 2990, "increment": 39, "is_bonus": false, "bonus_message": ""}}],
    [528, {"left": {"total": 3342, "increment": 44, "is_bonus": false, "bonus_message": ""}, "right": {"total": 3016, "increment": 26, "is_bonus": false, "bonus_message": ""}}],
    [528, {"left": {"total": 3382, "increment": 40, "is_bonus": false, "bonus_message": ""}, "right": {"total": 3036, "increment": 20, "is_bonus": false, "bonus_message": ""}}],
    [529, {"left": {"total": 3412, "increment": 30, "is_bonus": false, "bonus_message": ""}, "right": {"total": 3057, "increment": 21, "is_bonus": false, "bonus_message": ""}}],
    [530, {"left": {"total": 3440, "increment": 28, "is_bonus": false, "bonus_message": ""}, "right": {"total": 3078, "increment": 21, "is_bonus": false, "bonus_message": ""}}],
    [533, {"left": {"total": 4598, "increment": 1158, "is_bonus": true, "bonus_message": "soy-la-leche"}, "right": {"total": 3106, "increment": 28, "is_bonus": false, "bonus_message": ""}}],
    [534, {"left": {"total": 5770, "increment": 1172, "is_bonus": true, "bonus_message": "que-chulo"}, "right": {"total": 3151, "increment": 45, "is_bonus": false, "bonus_message": ""}}],
    [535, {"left": {"total": 5781, "increment": 11, "is_bonus": false, "bonus_message": ""}, "right": {"total": 5184, "increment": 2033, "is_bonus": true, "bonus_message": ""}}],
    [537, {"left": {"total": 5795, "increment": 14, "is_bonus": false, "bonus_message": ""}, "right": {"total": 5268, "increment": 84, "is_bonus": false, "bonus_message": ""}}],
    [539, {"left": {"total": 5827, "increment": 32, "is_bonus": false, "bonus_message": ""}, "right": {"total": 7317, "increment": 2049, "is_bonus": true, "bonus_message": "el-impacto"}}],
    [541, {"left": {"total": 5861, "increment": 34, "is_bonus": false, "bonus_message": ""}, "right": {"total": 7393, "increment": 76, "is_bonus": false, "bonus_message": ""}}],
    [542, {"left": {"total": 5886, "increment": 25, "is_bonus": false, "bonus_message": ""}, "right": {"total": 7479, "increment": 86, "is_bonus": false, "bonus_message": ""}}],
    [545, {"left": {"total": 5920, "increment": 34, "is_bonus": false, "bonus_message": ""}, "right": {"total": 7535, "increment": 56, "is_bonus": false, "bonus_message": ""}}],
    [546, "RIGHT WINS"],
    [546, {"left_lucha_pose": "loose"}],
    [546, {"right_lucha_pose": "win"}],
    [550, {"left_lucha_pose": "hidden"}],
    [550, {"right_lucha_pose": "hidden"}],
    [619, "battle_start"],
    [626, {"left": {"total": 0, "increment": 0, "is_bonus": false, "bonus_message": ""}, "right": {"total": 0, "increment": 0, "is_bonus": false, "bonus_message": ""}}],
    [629, {"left": {"total": 52, "increment": 52, "is_bonus": false, "bonus_message": ""}, "right": {"total": 340, "increment": 340, "is_bonus": false, "bonus_message": ""}}],
    [633, {"left": {"total": 92, "increment": 40, "is_bonus": false, "bonus_message": ""}, "right": {"total": 399, "increment": 59, "is_bonus": false, "bonus_message": ""}}],
    [636, {"left": {"total": 210, "increment": 118, "is_bonus": false, "bonus_message": ""}, "right": {"total": 484, "increment": 85, "is_bonus": false, "bonus_message": ""}}],
    [639, {"left": {"total": 319, "increment": 109, "is_bonus": false, "bonus_message": ""}, "right": {"total": 539, "increment": 55, "is_bonus": false, "bonus_message": ""}}],
    [642, {"left": {"total": 407, "increment": 88, "is_bonus": false, "bonus_message": ""}, "right": {"total": 614, "increment": 75, "is_bonus": false, "bonus_message": ""}}],
    [647, {"left": {"total": 449, "increment": 42, "is_bonus": false, "bonus_message": ""}, "right": {"total": 743, "increment": 129, "is_bonus": false, "bonus_message": ""}}],
    [650, {"left": {"total": 535, "increment": 86, "is_bonus": false, "bonus_message": ""}, "right": {"total": 949, "increment": 206, "is_bonus": false, "bonus_message": ""}}],
    [653, {"left": {"total": 589, "increment": 54, "is_bonus": false, "bonus_message": ""}, "right": {"total": 1006, "increment": 57, "is_bonus": false, "bonus_message": ""}}],
    [657, {"left": {"total": 780, "increment": 191, "is_bonus": false, "bonus_message": ""}, "right": {"total": 1025, "increment": 19, "is_bonus": false, "bonus_message": ""}}],
    [659, {"left": {"total": 983, "increment": 203, "is_bonus": false, "bonus_message": ""}, "right": {"total": 1059, "increment": 34, "is_bonus": false, "bonus_message": ""}}],
    [662, {"left": {"total": 1080, "increment": 97, "is_bonus": false, "bonus_message": ""}, "right": {"total": 1200, "increment": 141, "is_bonus": false, "bonus_message": ""}}],
    [666, {"left": {"total": 1156, "increment": 76, "is_bonus": false, "bonus_message": ""}, "right": {"total": 1255, "increment": 55, "is_bonus": false, "bonus_message": ""}}],
    [668, {"left": {"total": 1353, "increment": 197, "is_bonus": false, "bonus_message": ""}, "right": {"total": 1353, "increment": 98, "is_bonus": false, "bonus_message": ""}}],
    [669, {"left": {"total": 1482, "increment": 129, "is_bonus": false, "bonus_message": ""}, "right": {"total": 1393, "increment": 40, "is_bonus": false, "bonus_message": ""}}],
    [671, {"left": {"total": 1529, "increment": 47, "is_bonus": false, "bonus_message": ""}, "right": {"total": 1418, "increment": 25, "is_bonus": false, "bonus_message": ""}}],
    [674, {"left": {"total": 1586, "increment": 57, "is_bonus": false, "bonus_message": ""}, "right": {"total": 1471, "increment": 53, "is_bonus": false, "bonus_message": ""}}],
    [676, {"left": {"total": 1611, "increment": 25, "is_bonus": false, "bonus_message": ""}, "right": {"total": 1538, "increment": 67, "is_bonus": false, "bonus_message": ""}}],
    [681, {"left": {"total": 1637, "increment": 26, "is_bonus": false, "bonus_message": ""}, "right": {"total": 2300, "increment": 762, "is_bonus": true, "bonus_message": ""}}],
    [683, {"left": {"total": 1731, "increment": 94, "is_bonus": false, "bonus_message": ""}, "right": {"total": 2389, "increment": 89, "is_bonus": false, "bonus_message": ""}}],
    [686, {"left": {"total": 1768, "increment": 37, "is_bonus": false, "bonus_message": ""}, "right": {"total": 2436, "increment": 47, "is_bonus": false, "bonus_message": ""}}],
    [688, {"left": {"total": 1808, "increment": 40, "is_bonus": false, "bonus_message": ""}, "right": {"total": 2492, "increment": 56, "is_bonus": false, "bonus_message": ""}}],
    [689, {"left": {"total": 1858, "increment": 50, "is_bonus": false, "bonus_message": ""}, "right": {"total": 2546, "increment": 54, "is_bonus": false, "bonus_message": ""}}],
    [691, {"left": {"total": 1869, "increment": 11, "is_bonus": false, "bonus_message": ""}, "right": {"total": 2612, "increment": 66, "is_bonus": false, "bonus_message": ""}}],
    [693, {"left": {"total": 1887, "increment": 18, "is_bonus": false, "bonus_message": ""}, "right": {"total": 2733, "increment": 121, "is_bonus": false, "bonus_message": ""}}],
    [695, {"left": {"total": 1937, "increment": 50, "is_bonus": false, "bonus_message": ""}, "right": {"total": 2783, "increment": 50, "is_bonus": false, "bonus_message": ""}}],
    [696, {"left": {"total": 1984, "increment": 47, "is_bonus": false, "bonus_message": ""}, "right": {"total": 2847, "increment": 64, "is_bonus": false, "bonus_message": ""}}],
    [697, {"left": {"total": 2003, "increment": 19, "is_bonus": false, "bonus_message": ""}, "right": {"total": 2883, "increment": 36, "is_bonus": false, "bonus_message": ""}}],
    [699, {"left": {"total": 2029, "increment": 26, "is_bonus": false, "bonus_message": ""}, "right": {"total": 2912, "increment": 29, "is_bonus": false, "bonus_message": ""}}],
    [699, {"left": {"total": 2060, "increment": 31, "is_bonus": false, "bonus_message": ""}, "right": {"total": 2960, "increment": 48, "is_bonus": false, "bonus_message": ""}}],
    [700, {"left": {"total": 2096, "increment": 36, "is_bonus": false, "bonus_message": ""}, "right": {"total": 3017, "increment": 57, "is_bonus": false, "bonus_message": ""}}],
    [701, {"left": {"total": 2118, "increment": 22, "is_bonus": false, "bonus_message": ""}, "right": {"total": 3066, "increment": 49, "is_bonus": false, "bonus_message": ""}}],
    [702, {"left": {"total": 2142, "increment": 24, "is_bonus": false, "bonus_message": ""}, "right": {"total": 3106, "increment": 40, "is_bonus": false, "bonus_message": ""}}],
    [704, {"left": {"total": 2164, "increment": 22, "is_bonus": false, "bonus_message": ""}, "right": {"total": 3143, "increment": 37, "is_bonus": false, "bonus_message": ""}}],
    [705, {"left": {"total": 3350, "increment": 1186, "is_bonus": true, "bonus_message": ""}, "right": {"total": 3182, "increment": 39, "is_bonus": false, "bonus_message": ""}}],
    [707, {"left": {"total": 3385, "increment": 35, "is_bonus": false, "bonus_message": ""}, "right": {"total": 3200, "increment": 18, "is_bonus": false, "bonus_message": ""}}],
    [708, {"left": {"total": 3444, "increment": 59, "is_bonus": false, "bonus_message": ""}, "right": {"total": 3232, "increment": 32, "is_bonus": false, "bonus_message": ""}}],
    [709, {"left": {"total": 3479, "increment": 35, "is_bonus": false, "bonus_message": ""}, "right": {"total": 3249, "increment": 17, "is_bonus": false, "bonus_message": ""}}],
    [710, {"left": {"total": 3530, "increment": 51, "is_bonus": false, "bonus_message": ""}, "right": {"total": 3280, "increment": 31, "is_bonus": false, "bonus_message": ""}}],
    [712, {"left": {"total": 3559, "increment": 29, "is_bonus": false, "bonus_message": ""}, "right": {"total": 4526, "increment": 1246, "is_bonus": true, "bonus_message": ""}}],
    [714, {"left": {"total": 3618, "increment": 59, "is_bonus": false, "bonus_message": ""}, "right": {"total": 5818, "increment": 1292, "is_bonus": true, "bonus_message": ""}}],
    [716, {"left": {"total": 3661, "increment": 43, "is_bonus": false, "bonus_message": ""}, "right": {"total": 5847, "increment": 29, "is_bonus": false, "bonus_message": ""}}],
    [719, {"left": {"total": 3702, "increment": 41, "is_bonus": false, "bonus_message": ""}, "right": {"total": 5853, "increment": 6, "is_bonus": false, "bonus_message": ""}}],
    [721, {"left": {"total": 3719, "increment": 17, "is_bonus": false, "bonus_message": ""}, "right": {"total": 5854, "increment": 1, "is_bonus": false, "bonus_message": ""}}],
    [723, {"left": {"total": 3725, "increment": 6, "is_bonus": false, "bonus_message": ""}, "right": {"total": 5857, "increment": 3, "is_bonus": false, "bonus_message": ""}}],
    [725, {"left": {"total": 3727, "increment": 2, "is_bonus": false, "bonus_message": ""}, "right": {"total": 5859, "increment": 2, "is_bonus": false, "bonus_message": ""}}],
    [729, {"left": {"total": 3727, "increment": 0, "is_bonus": false, "bonus_message": ""}, "right": {"total": 5861, "increment": 2, "is_bonus": false, "bonus_message": ""}}],
    [732, {"left": {"total": 3728, "increment": 1, "is_bonus": false, "bonus_message": ""}, "right": {"total": 5866, "increment": 5, "is_bonus": false, "bonus_message": ""}}],
    [733, {"left": {"total": 3729, "increment": 1, "is_bonus": false, "bonus_message": ""}, "right": {"total": 5866, "increment": 0, "is_bonus": false, "bonus_message": ""}}],
    [734, {"left": {"total": 3729, "increment": 0, "is_bonus": false, "bonus_message": ""}, "right": {"total": 5866, "increment": 0, "is_bonus": false, "bonus_message": ""}}],
    [735, {"left": {"total": 3729, "increment": 0, "is_bonus": false, "bonus_message": ""}, "right": {"total": 5866, "increment": 0, "is_bonus": false, "bonus_message": ""}}],
    [736, {"left": {"total": 3731, "increment": 2, "is_bonus": false, "bonus_message": ""}, "right": {"total": 5867, "increment": 1, "is_bonus": false, "bonus_message": ""}}],
    [737, {"left": {"total": 3732, "increment": 1, "is_bonus": false, "bonus_message": ""}, "right": {"total": 5868, "increment": 1, "is_bonus": false, "bonus_message": ""}}],
    [738, {"left": {"total": 3734, "increment": 2, "is_bonus": false, "bonus_message": ""}, "right": {"total": 5868, "increment": 0, "is_bonus": false, "bonus_message": ""}}],
    [739, {"left": {"total": 3735, "increment": 1, "is_bonus": false, "bonus_message": ""}, "right": {"total": 5869, "increment": 1, "is_bonus": false, "bonus_message": ""}}],
    [740, {"left": {"total": 3735, "increment": 0, "is_bonus": false, "bonus_message": ""}, "right": {"total": 5869, "increment": 0, "is_bonus": false, "bonus_message": ""}}],
    [741, {"left": {"total": 3737, "increment": 2, "is_bonus": false, "bonus_message": ""}, "right": {"total": 5870, "increment": 1, "is_bonus": false, "bonus_message": ""}}],
    [743, {"left": {"total": 3740, "increment": 3, "is_bonus": false, "bonus_message": ""}, "right": {"total": 5875, "increment": 5, "is_bonus": false, "bonus_message": ""}}],
    [744, {"left": {"total": 3741, "increment": 1, "is_bonus": false, "bonus_message": ""}, "right": {"total": 5875, "increment": 0, "is_bonus": false, "bonus_message": ""}}],
    [746, {"left": {"total": 3742, "increment": 1, "is_bonus": false, "bonus_message": ""}, "right": {"total": 5878, "increment": 3, "is_bonus": false, "bonus_message": ""}}],
    [746, {"left": {"total": 3743, "increment": 1, "is_bonus": false, "bonus_message": ""}, "right": {"total": 5879, "increment": 1, "is_bonus": false, "bonus_message": ""}}],
    [747, {"left": {"total": 3744, "increment": 1, "is_bonus": false, "bonus_message": ""}, "right": {"total": 5883, "increment": 4, "is_bonus": false, "bonus_message": ""}}],
    [748, {"left": {"total": 3746, "increment": 2, "is_bonus": false, "bonus_message": ""}, "right": {"total": 5885, "increment": 2, "is_bonus": false, "bonus_message": ""}}],
    [749, {"left": {"total": 3747, "increment": 1, "is_bonus": false, "bonus_message": ""}, "right": {"total": 5887, "increment": 2, "is_bonus": false, "bonus_message": ""}}],
    [750, {"left": {"total": 3748, "increment": 1, "is_bonus": false, "bonus_message": ""}, "right": {"total": 5888, "increment": 1, "is_bonus": false, "bonus_message": ""}}],
    [751, "RIGHT WINS"],
    [774, "QUARTER FINALS"],
    [776, "battle_start"],
    [776, {"left_lucha_pose": "normal"}],
    [776, {"right_lucha_pose": "normal"}],
    [776, {"left": {"total": 0, "increment": 0, "is_bonus": false, "bonus_message": ""}, "right": {"total": 0, "increment": 0, "is_bonus": false, "bonus_message": ""}}],
    [778, {"left": {"total": 2, "increment": 2, "is_bonus": false, "bonus_message": ""}, "right": {"total": 0, "increment": 0, "is_bonus": false, "bonus_message": ""}}],
    [779, {"left": {"total": 2, "increment": 2, "is_bonus": false, "bonus_message": ""}, "right": {"total": 2, "increment": 2, "is_bonus": false, "bonus_message": ""}}],
    [780, {"left": {"total": 3, "increment": 1, "is_bonus": false, "bonus_message": ""}, "right": {"total": 8, "increment": 6, "is_bonus": false, "bonus_message": ""}}],
    [782, {"left": {"total": 5, "increment": 2, "is_bonus": false, "bonus_message": ""}, "right": {"total": 15, "increment": 7, "is_bonus": false, "bonus_message": ""}}],
    [784, {"left": {"total": 13, "increment": 8, "is_bonus": false, "bonus_message": ""}, "right": {"total": 41, "increment": 26, "is_bonus": false, "bonus_message": ""}}],
    [786, {"left": {"total": 22, "increment": 9, "is_bonus": false, "bonus_message": ""}, "right": {"total": 50, "increment": 9, "is_bonus": false, "bonus_message": ""}}],
    [787, {"left": {"total": 35, "increment": 13, "is_bonus": false, "bonus_message": ""}, "right": {"total": 86, "increment": 36, "is_bonus": false, "bonus_message": ""}}],
    [788, {"left": {"total": 39, "increment": 4, "is_bonus": false, "bonus_message": ""}, "right": {"total": 106, "increment": 20, "is_bonus": false, "bonus_message": ""}}],
    [790, {"left": {"total": 49, "increment": 10, "is_bonus": false, "bonus_message": ""}, "right": {"total": 130, "increment": 24, "is_bonus": false, "bonus_message": ""}}],
    [792, {"left": {"total": 68, "increment": 19, "is_bonus": false, "bonus_message": ""}, "right": {"total": 183, "increment": 53, "is_bonus": false, "bonus_message": ""}}],
    [793, {"left": {"total": 83, "increment": 15, "is_bonus": false, "bonus_message": ""}, "right": {"total": 253, "increment": 70, "is_bonus": false, "bonus_message": ""}}],
    [794, {"left": {"total": 95, "increment": 12, "is_bonus": false, "bonus_message": ""}, "right": {"total": 279, "increment": 26, "is_bonus": false, "bonus_message": ""}}],
    [796, {"left": {"total": 112, "increment": 17, "is_bonus": false, "bonus_message": ""}, "right": {"total": 306, "increment": 27, "is_bonus": false, "bonus_message": ""}}],
    [797, {"left": {"total": 236, "increment": 124, "is_bonus": true, "bonus_message": "soy-la-leche"}, "right": {"total": 343, "increment": 37, "is_bonus": false, "bonus_message": ""}}],
    [799, {"left": {"total": 245, "increment": 9, "is_bonus": false, "bonus_message": ""}, "right": {"total": 356, "increment": 13, "is_bonus": false, "bonus_message": ""}}],
    [800, {"left": {"total": 253, "increment": 8, "is_bonus": false, "bonus_message": ""}, "right": {"total": 365, "increment": 9, "is_bonus": false, "bonus_message": ""}}],
    [801, {"left": {"total": 261, "increment": 8, "is_bonus": false, "bonus_message": ""}, "right": {"total": 393, "increment": 28, "is_bonus": false, "bonus_message": ""}}],
    [802, "RIGHT WINS"],
    [802, {"left_lucha_pose": "loose"}],
    [802, {"right_lucha_pose": "win"}],
    [805, "battle_start"],
    [805, {"left_lucha_pose": "normal"}],
    [805, {"right_lucha_pose": "normal"}],
    [809, {"left": {"total": 8, "increment": 8, "is_bonus": false, "bonus_message": ""}, "right": {"total": 9, "increment": 9, "is_bonus": false, "bonus_message": ""}}],
    [811, {"left": {"total": 73, "increment": 73, "is_bonus": false, "bonus_message": ""}, "right": {"total": 52, "increment": 52, "is_bonus": false, "bonus_message": ""}}],
    [812, {"left": {"total": 114, "increment": 41, "is_bonus": false, "bonus_message": ""}, "right": {"total": 72, "increment": 20, "is_bonus": false, "bonus_message": ""}}],
    [813, {"left": {"total": 132, "increment": 18, "is_bonus": false, "bonus_message": ""}, "right": {"total": 85, "increment": 13, "is_bonus": false, "bonus_message": ""}}],
    [814, {"left": {"total": 151, "increment": 19, "is_bonus": false, "bonus_message": ""}, "right": {"total": 96, "increment": 11, "is_bonus": false, "bonus_message": ""}}],
    [816, {"left": {"total": 169, "increment": 18, "is_bonus": false, "bonus_message": ""}, "right": {"total": 103, "increment": 7, "is_bonus": false, "bonus_message": ""}}],
    [816, {"left": {"total": 188, "increment": 19, "is_bonus": false, "bonus_message": ""}, "right": {"total": 111, "increment": 8, "is_bonus": false, "bonus_message": ""}}],
    [817, {"left": {"total": 208, "increment": 20, "is_bonus": false, "bonus_message": ""}, "right": {"total": 118, "increment": 7, "is_bonus": false, "bonus_message": ""}}],
    [818, {"left": {"total": 224, "increment": 16, "is_bonus": false, "bonus_message": ""}, "right": {"total": 126, "increment": 8, "is_bonus": false, "bonus_message": ""}}],
    [819, {"left": {"total": 243, "increment": 19, "is_bonus": false, "bonus_message": ""}, "right": {"total": 144, "increment": 18, "is_bonus": false, "bonus_message": ""}}],
    [820, {"left": {"total": 261, "increment": 18, "is_bonus": false, "bonus_message": ""}, "right": {"total": 157, "increment": 13, "is_bonus": false, "bonus_message": ""}}],
    [821, {"left": {"total": 283, "increment": 22, "is_bonus": false, "bonus_message": ""}, "right": {"total": 166, "increment": 9, "is_bonus": false, "bonus_message": ""}}],
    [822, {"left": {"total": 303, "increment": 20, "is_bonus": false, "bonus_message": ""}, "right": {"total": 177, "increment": 11, "is_bonus": false, "bonus_message": ""}}],
    [823, "LEFT WINS"],
    [823, {"left_lucha_pose": "win"}],
    [823, {"right_lucha_pose": "loose"}],
    [826, "battle_start"],
    [826, {"left_lucha_pose": "normal"}],
    [826, {"right_lucha_pose": "normal"}],
    [827, {"left": {"total": 6, "increment": 6, "is_bonus": false, "bonus_message": ""}, "right": {"total": 11, "increment": 11, "is_bonus": false, "bonus_message": ""}}],
    [829, {"left": {"total": 13, "increment": 7, "is_bonus": false, "bonus_message": ""}, "right": {"total": 36, "increment": 25, "is_bonus": false, "bonus_message": ""}}],
    [833, {"left": {"total": 18, "increment": 5, "is_bonus": false, "bonus_message": ""}, "right": {"total": 106, "increment": 70, "is_bonus": false, "bonus_message": ""}}],
    [836, {"left": {"total": 33, "increment": 15, "is_bonus": false, "bonus_message": ""}, "right": {"total": 243, "increment": 137, "is_bonus": false, "bonus_message": ""}}],
    [837, {"left": {"total": 48, "increment": 15, "is_bonus": false, "bonus_message": ""}, "right": {"total": 315, "increment": 72, "is_bonus": false, "bonus_message": ""}}],
    [839, {"left": {"total": 55, "increment": 7, "is_bonus": false, "bonus_message": ""}, "right": {"total": 336, "increment": 21, "is_bonus": false, "bonus_message": ""}}],
    [840, "RIGHT WINS"],
    [840, {"left_lucha_pose": "loose"}],
    [840, {"right_lucha_pose": "win"}],
    [852, {"left": {"total": 77, "increment": 22, "is_bonus": false, "bonus_message": ""}, "right": {"total": 386, "increment": 50, "is_bonus": false, "bonus_message": ""}}],
    // [855, "RIGHT WINS"],
    [900, "battle_start"],
    [900, {"left_lucha_pose": "hidden"}],
    [900, {"right_lucha_pose": "hidden"}],
    [902, "oopse"],
    // [986, "battle_start"],
    [977, {"left_lucha_pose": "normal"}],
    [977, {"right_lucha_pose": "normal"}],
    [978, "BATTLE START"],
    [986, {"left": {"total": 50, "increment": 50, "is_bonus": false, "bonus_message": ""}, "right": {"total": 38, "increment": 38, "is_bonus": false, "bonus_message": ""}}],
    [987, {"left": {"total": 67, "increment": 17, "is_bonus": false, "bonus_message": ""}, "right": {"total": 52, "increment": 14, "is_bonus": false, "bonus_message": ""}}],
    [988, {"left": {"total": 27, "increment": 27, "is_bonus": false, "bonus_message": ""}, "right": {"total": 8, "increment": 8, "is_bonus": false, "bonus_message": ""}}],
    [989, {"left": {"total": 43, "increment": 16, "is_bonus": false, "bonus_message": ""}, "right": {"total": 18, "increment": 10, "is_bonus": false, "bonus_message": ""}}],
    [990, {"left": {"total": 67, "increment": 24, "is_bonus": false, "bonus_message": ""}, "right": {"total": 29, "increment": 11, "is_bonus": false, "bonus_message": ""}}],
    [991, {"left": {"total": 97, "increment": 30, "is_bonus": false, "bonus_message": ""}, "right": {"total": 43, "increment": 14, "is_bonus": false, "bonus_message": ""}}],
    [992, {"left": {"total": 116, "increment": 19, "is_bonus": false, "bonus_message": ""}, "right": {"total": 65, "increment": 22, "is_bonus": false, "bonus_message": ""}}],
    [993, {"left": {"total": 136, "increment": 20, "is_bonus": false, "bonus_message": ""}, "right": {"total": 89, "increment": 24, "is_bonus": false, "bonus_message": ""}}],
    [994, {"left": {"total": 149, "increment": 13, "is_bonus": false, "bonus_message": ""}, "right": {"total": 107, "increment": 18, "is_bonus": false, "bonus_message": ""}}],
    [995, {"left": {"total": 167, "increment": 18, "is_bonus": false, "bonus_message": ""}, "right": {"total": 132, "increment": 25, "is_bonus": false, "bonus_message": ""}}],
    [996, {"left": {"total": 186, "increment": 19, "is_bonus": false, "bonus_message": ""}, "right": {"total": 156, "increment": 24, "is_bonus": false, "bonus_message": ""}}],
    [997, {"left": {"total": 200, "increment": 14, "is_bonus": false, "bonus_message": ""}, "right": {"total": 178, "increment": 22, "is_bonus": false, "bonus_message": ""}}],
    [1000, {"left": {"total": 218, "increment": 18, "is_bonus": false, "bonus_message": ""}, "right": {"total": 196, "increment": 18, "is_bonus": false, "bonus_message": ""}}],
    [1002, {"left": {"total": 378, "increment": 160, "is_bonus": true, "bonus_message": "soy-la-leche"}, "right": {"total": 337, "increment": 141, "is_bonus": true, "bonus_message": ""}}],
    [1003, {"left": {"total": 538, "increment": 160, "is_bonus": true, "bonus_message": "el-impacto"}, "right": {"total": 363, "increment": 26, "is_bonus": false, "bonus_message": ""}}],
    [1004, {"left": {"total": 559, "increment": 21, "is_bonus": false, "bonus_message": ""}, "right": {"total": 373, "increment": 10, "is_bonus": false, "bonus_message": ""}}],
    [1005, {"left": {"total": 575, "increment": 16, "is_bonus": false, "bonus_message": ""}, "right": {"total": 382, "increment": 9, "is_bonus": false, "bonus_message": ""}}],
    [1007, {"left": {"total": 592, "increment": 17, "is_bonus": false, "bonus_message": ""}, "right": {"total": 389, "increment": 7, "is_bonus": false, "bonus_message": ""}}],
    [1008, "LEFT WINS"],
    [1008, {"left_lucha_pose": "win"}],
    [1008, {"right_lucha_pose": "loose"}],
    [1034, "battle_start"],
    [1034, {"left_lucha_pose": "normal"}],
    [1034, {"right_lucha_pose": "normal"}],
    [1034, {"left": {"total": 7, "increment": 7, "is_bonus": false, "bonus_message": ""}, "right": {"total": 8, "increment": 8, "is_bonus": false, "bonus_message": ""}}],
    [1035, {"left": {"total": 8, "increment": 8, "is_bonus": false, "bonus_message": ""}, "right": {"total": 14, "increment": 14, "is_bonus": false, "bonus_message": ""}}],
    [1037, {"left": {"total": 17, "increment": 9, "is_bonus": false, "bonus_message": ""}, "right": {"total": 22, "increment": 8, "is_bonus": false, "bonus_message": ""}}],
    [1038, {"left": {"total": 38, "increment": 21, "is_bonus": false, "bonus_message": ""}, "right": {"total": 57, "increment": 35, "is_bonus": false, "bonus_message": ""}}],
    [1039, {"left": {"total": 50, "increment": 12, "is_bonus": false, "bonus_message": ""}, "right": {"total": 72, "increment": 15, "is_bonus": false, "bonus_message": ""}}],
    [1040, {"left": {"total": 63, "increment": 13, "is_bonus": false, "bonus_message": ""}, "right": {"total": 90, "increment": 18, "is_bonus": false, "bonus_message": ""}}],
    [1041, {"left": {"total": 73, "increment": 10, "is_bonus": false, "bonus_message": ""}, "right": {"total": 111, "increment": 21, "is_bonus": false, "bonus_message": ""}}],
    [1043, {"left": {"total": 84, "increment": 11, "is_bonus": false, "bonus_message": ""}, "right": {"total": 131, "increment": 20, "is_bonus": false, "bonus_message": ""}}],
    [1044, {"left": {"total": 106, "increment": 22, "is_bonus": false, "bonus_message": ""}, "right": {"total": 158, "increment": 27, "is_bonus": false, "bonus_message": ""}}],
    [1046, {"left": {"total": 116, "increment": 10, "is_bonus": false, "bonus_message": ""}, "right": {"total": 169, "increment": 11, "is_bonus": false, "bonus_message": ""}}],
    [1047, {"left": {"total": 173, "increment": 57, "is_bonus": false, "bonus_message": ""}, "right": {"total": 190, "increment": 21, "is_bonus": false, "bonus_message": ""}}],
    [1049, {"left": {"total": 211, "increment": 38, "is_bonus": false, "bonus_message": ""}, "right": {"total": 203, "increment": 13, "is_bonus": false, "bonus_message": ""}}],
    [1050, {"left": {"total": 367, "increment": 156, "is_bonus": true, "bonus_message": ""}, "right": {"total": 229, "increment": 26, "is_bonus": false, "bonus_message": ""}}],
    [1051, {"left": {"total": 388, "increment": 21, "is_bonus": false, "bonus_message": ""}, "right": {"total": 238, "increment": 9, "is_bonus": false, "bonus_message": ""}}],
    [1053, {"left": {"total": 405, "increment": 17, "is_bonus": false, "bonus_message": ""}, "right": {"total": 249, "increment": 11, "is_bonus": false, "bonus_message": ""}}],
    [1053, {"left": {"total": 429, "increment": 24, "is_bonus": false, "bonus_message": ""}, "right": {"total": 257, "increment": 8, "is_bonus": false, "bonus_message": ""}}],
    [1055, {"left": {"total": 440, "increment": 11, "is_bonus": false, "bonus_message": ""}, "right": {"total": 268, "increment": 11, "is_bonus": false, "bonus_message": ""}}],
    [1056, {"left": {"total": 465, "increment": 25, "is_bonus": false, "bonus_message": ""}, "right": {"total": 294, "increment": 26, "is_bonus": false, "bonus_message": ""}}],
    [1057, {"left": {"total": 482, "increment": 17, "is_bonus": false, "bonus_message": ""}, "right": {"total": 307, "increment": 13, "is_bonus": false, "bonus_message": ""}}],
    [1058, {"left": {"total": 499, "increment": 17, "is_bonus": false, "bonus_message": ""}, "right": {"total": 507, "increment": 200, "is_bonus": true, "bonus_message": ""}}],
    [1059, {"left": {"total": 515, "increment": 16, "is_bonus": false, "bonus_message": ""}, "right": {"total": 709, "increment": 202, "is_bonus": true, "bonus_message": ""}}],
    [1060, {"left": {"total": 528, "increment": 13, "is_bonus": false, "bonus_message": ""}, "right": {"total": 743, "increment": 34, "is_bonus": false, "bonus_message": ""}}],
    [1061, {"left": {"total": 541, "increment": 13, "is_bonus": false, "bonus_message": ""}, "right": {"total": 758, "increment": 15, "is_bonus": false, "bonus_message": ""}}],
    [1062, {"left": {"total": 556, "increment": 15, "is_bonus": false, "bonus_message": ""}, "right": {"total": 769, "increment": 11, "is_bonus": false, "bonus_message": ""}}],
    [1063, {"left": {"total": 569, "increment": 13, "is_bonus": false, "bonus_message": ""}, "right": {"total": 784, "increment": 15, "is_bonus": false, "bonus_message": ""}}],
    [1069, {"left": {"total": 585, "increment": 16, "is_bonus": false, "bonus_message": ""}, "right": {"total": 792, "increment": 8, "is_bonus": false, "bonus_message": ""}}],
    [1071, {"left": {"total": 959, "increment": 374, "is_bonus": true, "bonus_message": ""}, "right": {"total": 1079, "increment": 287, "is_bonus": true, "bonus_message": ""}}],
    [1073, {"left": {"total": 996, "increment": 37, "is_bonus": false, "bonus_message": ""}, "right": {"total": 1114, "increment": 35, "is_bonus": false, "bonus_message": ""}}],
    [1075, {"left": {"total": 1027, "increment": 31, "is_bonus": false, "bonus_message": ""}, "right": {"total": 1141, "increment": 27, "is_bonus": false, "bonus_message": ""}}],
    [1077, {"left": {"total": 1069, "increment": 42, "is_bonus": false, "bonus_message": ""}, "right": {"total": 1174, "increment": 33, "is_bonus": false, "bonus_message": ""}}],
    [1079, {"left": {"total": 1104, "increment": 35, "is_bonus": false, "bonus_message": ""}, "right": {"total": 1208, "increment": 34, "is_bonus": false, "bonus_message": ""}}],
    [1082, {"left": {"total": 1124, "increment": 20, "is_bonus": false, "bonus_message": ""}, "right": {"total": 1648, "increment": 440, "is_bonus": true, "bonus_message": ""}}],
    [1084, {"left": {"total": 1160, "increment": 36, "is_bonus": false, "bonus_message": ""}, "right": {"total": 2135, "increment": 487, "is_bonus": true, "bonus_message": ""}}],
    [1086, {"left": {"total": 1180, "increment": 20, "is_bonus": false, "bonus_message": ""}, "right": {"total": 2178, "increment": 43, "is_bonus": false, "bonus_message": ""}}],
    [1088, {"left": {"total": 1210, "increment": 30, "is_bonus": false, "bonus_message": ""}, "right": {"total": 2220, "increment": 42, "is_bonus": false, "bonus_message": ""}}],
    [1089, {"left": {"total": 1248, "increment": 38, "is_bonus": false, "bonus_message": ""}, "right": {"total": 2250, "increment": 30, "is_bonus": false, "bonus_message": ""}}],
    [1090, {"left": {"total": 1264, "increment": 16, "is_bonus": false, "bonus_message": ""}, "right": {"total": 2270, "increment": 20, "is_bonus": false, "bonus_message": ""}}],
    [1092, {"left": {"total": 1279, "increment": 15, "is_bonus": false, "bonus_message": ""}, "right": {"total": 2289, "increment": 19, "is_bonus": false, "bonus_message": ""}}],
    [1093, {"left": {"total": 1300, "increment": 21, "is_bonus": false, "bonus_message": ""}, "right": {"total": 2343, "increment": 54, "is_bonus": false, "bonus_message": ""}}],
    [1094, "RIGHT WINS"],
    [1094, {"left_lucha_pose": "loose"}],
    [1094, {"right_lucha_pose": "win"}],
    [1100, {"left_lucha_pose": "hidden"}],
    [1100, {"right_lucha_pose": "hidden"}],
    [1167, "SEMI FINALS 1"],
    [1169, "battle_start"],
    [1169, {"left_lucha_pose": "normal"}],
    [1169, {"right_lucha_pose": "normal"}],
    [1169, {"left": {"total": 0, "increment": 0, "is_bonus": false, "bonus_message": ""}, "right": {"total": 1, "increment": 1, "is_bonus": false, "bonus_message": ""}}],
    [1170, {"left": {"total": 0, "increment": 0, "is_bonus": false, "bonus_message": ""}, "right": {"total": 1, "increment": 0, "is_bonus": false, "bonus_message": ""}}],
    [1171, {"left": {"total": 3, "increment": 3, "is_bonus": false, "bonus_message": ""}, "right": {"total": 2, "increment": 1, "is_bonus": false, "bonus_message": ""}}],
    [1172, {"left": {"total": 5, "increment": 2, "is_bonus": false, "bonus_message": ""}, "right": {"total": 5, "increment": 3, "is_bonus": false, "bonus_message": ""}}],
    [1174, {"left": {"total": 9, "increment": 4, "is_bonus": false, "bonus_message": ""}, "right": {"total": 8, "increment": 3, "is_bonus": false, "bonus_message": ""}}],
    [1176, {"left": {"total": 21, "increment": 12, "is_bonus": false, "bonus_message": ""}, "right": {"total": 20, "increment": 12, "is_bonus": false, "bonus_message": ""}}],
    [1178, {"left": {"total": 38, "increment": 17, "is_bonus": false, "bonus_message": ""}, "right": {"total": 35, "increment": 15, "is_bonus": false, "bonus_message": ""}}],
    [1180, {"left": {"total": 52, "increment": 14, "is_bonus": false, "bonus_message": ""}, "right": {"total": 61, "increment": 26, "is_bonus": false, "bonus_message": ""}}],
    [1181, {"left": {"total": 72, "increment": 20, "is_bonus": false, "bonus_message": ""}, "right": {"total": 94, "increment": 33, "is_bonus": false, "bonus_message": ""}}],
    [1182, {"left": {"total": 81, "increment": 9, "is_bonus": false, "bonus_message": ""}, "right": {"total": 117, "increment": 23, "is_bonus": false, "bonus_message": ""}}],
    [1185, {"left": {"total": 96, "increment": 15, "is_bonus": false, "bonus_message": ""}, "right": {"total": 138, "increment": 21, "is_bonus": false, "bonus_message": ""}}],
    [1186, {"left": {"total": 230, "increment": 134, "is_bonus": true, "bonus_message": ""}, "right": {"total": 289, "increment": 151, "is_bonus": true, "bonus_message": "que-chulo"}}],
    [1187, {"left": {"total": 241, "increment": 11, "is_bonus": false, "bonus_message": ""}, "right": {"total": 305, "increment": 16, "is_bonus": false, "bonus_message": ""}}],
    [1188, {"left": {"total": 254, "increment": 13, "is_bonus": false, "bonus_message": ""}, "right": {"total": 315, "increment": 10, "is_bonus": false, "bonus_message": ""}}],
    [1189, {"left": {"total": 263, "increment": 9, "is_bonus": false, "bonus_message": ""}, "right": {"total": 330, "increment": 15, "is_bonus": false, "bonus_message": ""}}],
    [1190, {"left": {"total": 277, "increment": 14, "is_bonus": false, "bonus_message": ""}, "right": {"total": 345, "increment": 15, "is_bonus": false, "bonus_message": ""}}],
    [1192, {"left": {"total": 287, "increment": 10, "is_bonus": false, "bonus_message": ""}, "right": {"total": 358, "increment": 13, "is_bonus": false, "bonus_message": ""}}],
    [1193, {"left": {"total": 433, "increment": 146, "is_bonus": true, "bonus_message": "que-chulo"}, "right": {"total": 384, "increment": 26, "is_bonus": false, "bonus_message": ""}}],
    [1194, {"left": {"total": 446, "increment": 13, "is_bonus": false, "bonus_message": ""}, "right": {"total": 407, "increment": 23, "is_bonus": false, "bonus_message": ""}}],
    [1195, {"left": {"total": 464, "increment": 18, "is_bonus": false, "bonus_message": ""}, "right": {"total": 422, "increment": 15, "is_bonus": false, "bonus_message": ""}}],
    [1196, {"left": {"total": 479, "increment": 15, "is_bonus": false, "bonus_message": ""}, "right": {"total": 431, "increment": 9, "is_bonus": false, "bonus_message": ""}}],
    [1197, {"left": {"total": 496, "increment": 17, "is_bonus": false, "bonus_message": ""}, "right": {"total": 444, "increment": 13, "is_bonus": false, "bonus_message": ""}}],
    [1198, {"left": {"total": 509, "increment": 13, "is_bonus": false, "bonus_message": ""}, "right": {"total": 457, "increment": 13, "is_bonus": false, "bonus_message": ""}}],
    [1199, {"left": {"total": 527, "increment": 18, "is_bonus": false, "bonus_message": ""}, "right": {"total": 666, "increment": 209, "is_bonus": true, "bonus_message": "soy-la-leche"}}],
    [1200, "RIGHT WINS"],
    [1200, {"left_lucha_pose": "loose"}],
    [1200, {"right_lucha_pose": "win"}],
    [1210, "battle_start"],
    [1210, {"left_lucha_pose": "hidden"}],
    [1210, {"right_lucha_pose": "hidden"}],
    [1210, {"left": {"total": 0, "increment": 0, "is_bonus": false, "bonus_message": ""}, "right": {"total": 3, "increment": 3, "is_bonus": false, "bonus_message": ""}}],
    [1211, {"left": {"total": 1, "increment": 1, "is_bonus": false, "bonus_message": ""}, "right": {"total": 4, "increment": 4, "is_bonus": false, "bonus_message": ""}}],
    [1212, {"left": {"total": 1, "increment": 1, "is_bonus": false, "bonus_message": ""}, "right": {"total": 2, "increment": 2, "is_bonus": false, "bonus_message": ""}}],
    [1213, {"left": {"total": 4, "increment": 3, "is_bonus": false, "bonus_message": ""}, "right": {"total": 3, "increment": 1, "is_bonus": false, "bonus_message": ""}}],
    [1214, {"left": {"total": 5, "increment": 1, "is_bonus": false, "bonus_message": ""}, "right": {"total": 5, "increment": 2, "is_bonus": false, "bonus_message": ""}}],
    [1216, {"left": {"total": 7, "increment": 2, "is_bonus": false, "bonus_message": ""}, "right": {"total": 7, "increment": 2, "is_bonus": false, "bonus_message": ""}}],
    [1218, {"left": {"total": 10, "increment": 3, "is_bonus": false, "bonus_message": ""}, "right": {"total": 15, "increment": 8, "is_bonus": false, "bonus_message": ""}}],
    [1219, {"left": {"total": 12, "increment": 2, "is_bonus": false, "bonus_message": ""}, "right": {"total": 18, "increment": 3, "is_bonus": false, "bonus_message": ""}}],
    [1221, {"left": {"total": 13, "increment": 1, "is_bonus": false, "bonus_message": ""}, "right": {"total": 22, "increment": 4, "is_bonus": false, "bonus_message": ""}}],
    [1222, {"left": {"total": 16, "increment": 3, "is_bonus": false, "bonus_message": ""}, "right": {"total": 31, "increment": 9, "is_bonus": false, "bonus_message": ""}}],
    [1223, {"left": {"total": 19, "increment": 3, "is_bonus": false, "bonus_message": ""}, "right": {"total": 36, "increment": 5, "is_bonus": false, "bonus_message": ""}}],
    [1224, {"left": {"total": 23, "increment": 4, "is_bonus": false, "bonus_message": ""}, "right": {"total": 40, "increment": 4, "is_bonus": false, "bonus_message": ""}}],
    [1225, {"left": {"total": 27, "increment": 4, "is_bonus": false, "bonus_message": ""}, "right": {"total": 43, "increment": 3, "is_bonus": false, "bonus_message": ""}}],
    [1226, {"left": {"total": 30, "increment": 3, "is_bonus": false, "bonus_message": ""}, "right": {"total": 48, "increment": 5, "is_bonus": false, "bonus_message": ""}}],
    [1227, {"left": {"total": 136, "increment": 106, "is_bonus": true, "bonus_message": "ay-caramba"}, "right": {"total": 50, "increment": 2, "is_bonus": false, "bonus_message": ""}}],
    [1228, {"left": {"total": 140, "increment": 4, "is_bonus": false, "bonus_message": ""}, "right": {"total": 53, "increment": 3, "is_bonus": false, "bonus_message": ""}}],
    [1229, "SEMI FINALS 2"],
    [1231, "BATTLE START"],
    [1231, {"left_lucha_pose": "normal"}],
    [1231, {"right_lucha_pose": "normal"}],
    [1231, {"left": {"total": 143, "increment": 3, "is_bonus": false, "bonus_message": ""}, "right": {"total": 55, "increment": 2, "is_bonus": false, "bonus_message": ""}}],
    [1232, {"left": {"total": 264, "increment": 121, "is_bonus": true, "bonus_message": "soy-la-leche"}, "right": {"total": 163, "increment": 108, "is_bonus": true, "bonus_message": ""}}],
    [1233, {"left": {"total": 378, "increment": 114, "is_bonus": true, "bonus_message": "soy-la-leche"}, "right": {"total": 170, "increment": 7, "is_bonus": false, "bonus_message": ""}}],
    [1234, {"left": {"total": 491, "increment": 113, "is_bonus": true, "bonus_message": ""}, "right": {"total": 307, "increment": 137, "is_bonus": true, "bonus_message": "el-impacto"}}],
    [1235, {"left": {"total": 622, "increment": 131, "is_bonus": true, "bonus_message": ""}, "right": {"total": 484, "increment": 177, "is_bonus": true, "bonus_message": "el-impacto"}}],
    [1236, {"left": {"total": 639, "increment": 17, "is_bonus": false, "bonus_message": ""}, "right": {"total": 493, "increment": 9, "is_bonus": false, "bonus_message": ""}}],
    [1238, {"left": {"total": 657, "increment": 18, "is_bonus": false, "bonus_message": ""}, "right": {"total": 719, "increment": 226, "is_bonus": true, "bonus_message": ""}}],
    [1239, {"left": {"total": 933, "increment": 276, "is_bonus": true, "bonus_message": "ay-caramba"}, "right": {"total": 956, "increment": 237, "is_bonus": true, "bonus_message": ""}}],
    [1240, {"left": {"total": 956, "increment": 23, "is_bonus": false, "bonus_message": ""}, "right": {"total": 963, "increment": 7, "is_bonus": false, "bonus_message": ""}}],
    [1241, {"left": {"total": 979, "increment": 23, "is_bonus": false, "bonus_message": ""}, "right": {"total": 974, "increment": 11, "is_bonus": false, "bonus_message": ""}}],
    [1242, {"left": {"total": 1003, "increment": 24, "is_bonus": false, "bonus_message": ""}, "right": {"total": 988, "increment": 14, "is_bonus": false, "bonus_message": ""}}],
    [1243, {"left": {"total": 1019, "increment": 16, "is_bonus": false, "bonus_message": ""}, "right": {"total": 998, "increment": 10, "is_bonus": false, "bonus_message": ""}}],
    [1244, {"left": {"total": 1038, "increment": 19, "is_bonus": false, "bonus_message": ""}, "right": {"total": 1013, "increment": 15, "is_bonus": false, "bonus_message": ""}}],
    [1245, {"left": {"total": 1054, "increment": 16, "is_bonus": false, "bonus_message": ""}, "right": {"total": 1395, "increment": 382, "is_bonus": true, "bonus_message": "andale"}}],
    [1246, {"left": {"total": 1060, "increment": 6, "is_bonus": false, "bonus_message": ""}, "right": {"total": 1773, "increment": 378, "is_bonus": true, "bonus_message": "soy-la-leche"}}],
    [1247, {"left": {"total": 1076, "increment": 16, "is_bonus": false, "bonus_message": ""}, "right": {"total": 1794, "increment": 21, "is_bonus": false, "bonus_message": ""}}],
    [1248, {"left": {"total": 1095, "increment": 19, "is_bonus": false, "bonus_message": ""}, "right": {"total": 1820, "increment": 26, "is_bonus": false, "bonus_message": ""}}],
    [1249, {"left": {"total": 1118, "increment": 23, "is_bonus": false, "bonus_message": ""}, "right": {"total": 1836, "increment": 16, "is_bonus": false, "bonus_message": ""}}],
    [1250, {"left": {"total": 1129, "increment": 11, "is_bonus": false, "bonus_message": ""}, "right": {"total": 1853, "increment": 17, "is_bonus": false, "bonus_message": ""}}],
    [1251, {"left": {"total": 1146, "increment": 17, "is_bonus": false, "bonus_message": ""}, "right": {"total": 1868, "increment": 15, "is_bonus": false, "bonus_message": ""}}],
    [1252, {"left": {"total": 1165, "increment": 19, "is_bonus": false, "bonus_message": ""}, "right": {"total": 1887, "increment": 19, "is_bonus": false, "bonus_message": ""}}],
    [1254, {"left": {"total": 1187, "increment": 22, "is_bonus": false, "bonus_message": ""}, "right": {"total": 1908, "increment": 21, "is_bonus": false, "bonus_message": ""}}],
    [1255, {"left": {"total": 1855, "increment": 668, "is_bonus": true, "bonus_message": "ay-caramba"}, "right": {"total": 2334, "increment": 426, "is_bonus": true, "bonus_message": ""}}],
    [1256, {"left": {"total": 1877, "increment": 22, "is_bonus": false, "bonus_message": ""}, "right": {"total": 2354, "increment": 20, "is_bonus": false, "bonus_message": ""}}],
    [1257, {"left": {"total": 1891, "increment": 14, "is_bonus": false, "bonus_message": ""}, "right": {"total": 2371, "increment": 17, "is_bonus": false, "bonus_message": ""}}],
    [1258, {"left": {"total": 1906, "increment": 15, "is_bonus": false, "bonus_message": ""}, "right": {"total": 2392, "increment": 21, "is_bonus": false, "bonus_message": ""}}],
    [1259, {"left": {"total": 1926, "increment": 20, "is_bonus": false, "bonus_message": ""}, "right": {"total": 2415, "increment": 23, "is_bonus": false, "bonus_message": ""}}],
    [1261, {"left": {"total": 1934, "increment": 8, "is_bonus": false, "bonus_message": ""}, "right": {"total": 2426, "increment": 11, "is_bonus": false, "bonus_message": ""}}],
    [1262, {"left": {"total": 2782, "increment": 848, "is_bonus": true, "bonus_message": "andale"}, "right": {"total": 3107, "increment": 681, "is_bonus": true, "bonus_message": ""}}],
    [1263, {"left": {"total": 2797, "increment": 15, "is_bonus": false, "bonus_message": ""}, "right": {"total": 3133, "increment": 26, "is_bonus": false, "bonus_message": ""}}],
    [1264, {"left": {"total": 2812, "increment": 15, "is_bonus": false, "bonus_message": ""}, "right": {"total": 3156, "increment": 23, "is_bonus": false, "bonus_message": ""}}],
    [1265, {"left": {"total": 2839, "increment": 27, "is_bonus": false, "bonus_message": ""}, "right": {"total": 3176, "increment": 20, "is_bonus": false, "bonus_message": ""}}],
    [1266, {"left": {"total": 2864, "increment": 25, "is_bonus": false, "bonus_message": ""}, "right": {"total": 3188, "increment": 12, "is_bonus": false, "bonus_message": ""}}],
    [1267, {"left": {"total": 2891, "increment": 27, "is_bonus": false, "bonus_message": ""}, "right": {"total": 3213, "increment": 25, "is_bonus": false, "bonus_message": ""}}],
    [1268, {"left": {"total": 2916, "increment": 25, "is_bonus": false, "bonus_message": ""}, "right": {"total": 3233, "increment": 20, "is_bonus": false, "bonus_message": ""}}],
    [1269, {"left": {"total": 2927, "increment": 11, "is_bonus": false, "bonus_message": ""}, "right": {"total": 3255, "increment": 22, "is_bonus": false, "bonus_message": ""}}],
    [1270, {"left": {"total": 2940, "increment": 13, "is_bonus": false, "bonus_message": ""}, "right": {"total": 3278, "increment": 23, "is_bonus": false, "bonus_message": ""}}],
    [1273, {"left": {"total": 2961, "increment": 21, "is_bonus": false, "bonus_message": ""}, "right": {"total": 3306, "increment": 28, "is_bonus": false, "bonus_message": ""}}],
    [1274, "RIGHT WINS"],
    [1274, {"left_lucha_pose": "loose"}],
    [1274, {"right_lucha_pose": "win"}],
    [1280, {"left_lucha_pose": "hidden"}],
    [1280, {"right_lucha_pose": "hidden"}],
    [1290, "battle_start"],
    [1290, {"left": {"total": 0, "increment": 0, "is_bonus": false, "bonus_message": ""}, "right": {"total": 0, "increment": 0, "is_bonus": false, "bonus_message": ""}}],
    [1291, {"left": {"total": 0, "increment": 0, "is_bonus": false, "bonus_message": ""}, "right": {"total": 0, "increment": 0, "is_bonus": false, "bonus_message": ""}}],
    [1292, {"left": {"total": 0, "increment": 0, "is_bonus": false, "bonus_message": ""}, "right": {"total": 2, "increment": 2, "is_bonus": false, "bonus_message": ""}}],
    [1293, {"left": {"total": 0, "increment": 0, "is_bonus": false, "bonus_message": ""}, "right": {"total": 5, "increment": 3, "is_bonus": false, "bonus_message": ""}}],
    [1294, {"left": {"total": 1, "increment": 1, "is_bonus": false, "bonus_message": ""}, "right": {"total": 7, "increment": 2, "is_bonus": false, "bonus_message": ""}}],
    [1295, {"left": {"total": 2, "increment": 1, "is_bonus": false, "bonus_message": ""}, "right": {"total": 7, "increment": 0, "is_bonus": false, "bonus_message": ""}}],
    [1296, {"left": {"total": 3, "increment": 1, "is_bonus": false, "bonus_message": ""}, "right": {"total": 10, "increment": 3, "is_bonus": false, "bonus_message": ""}}],
    [1297, {"left": {"total": 6, "increment": 3, "is_bonus": false, "bonus_message": ""}, "right": {"total": 12, "increment": 2, "is_bonus": false, "bonus_message": ""}}],
    [1298, {"left": {"total": 8, "increment": 2, "is_bonus": false, "bonus_message": ""}, "right": {"total": 15, "increment": 3, "is_bonus": false, "bonus_message": ""}}],
    [1299, "FINAL ROUND"],
    [1299, {"left": {"total": 12, "increment": 4, "is_bonus": false, "bonus_message": ""}, "right": {"total": 20, "increment": 5, "is_bonus": false, "bonus_message": ""}}],
    [1300, {"left": {"total": 16, "increment": 4, "is_bonus": false, "bonus_message": ""}, "right": {"total": 25, "increment": 5, "is_bonus": false, "bonus_message": ""}}],
    [1301, {"left": {"total": 20, "increment": 4, "is_bonus": false, "bonus_message": ""}, "right": {"total": 28, "increment": 3, "is_bonus": false, "bonus_message": ""}}],
    [1301, "BATTLE START"],
    [1301, {"left_lucha_pose": "normal"}],
    [1301, {"right_lucha_pose": "normal"}],
    [1302, {"left": {"total": 23, "increment": 3, "is_bonus": false, "bonus_message": ""}, "right": {"total": 32, "increment": 4, "is_bonus": false, "bonus_message": ""}}],
    [1303, {"left": {"total": 131, "increment": 108, "is_bonus": true, "bonus_message": "que-chulo"}, "right": {"total": 36, "increment": 4, "is_bonus": false, "bonus_message": ""}}],
    [1304, {"left": {"total": 238, "increment": 107, "is_bonus": true, "bonus_message": ""}, "right": {"total": 147, "increment": 111, "is_bonus": true, "bonus_message": ""}}],
    [1305, {"left": {"total": 350, "increment": 112, "is_bonus": true, "bonus_message": ""}, "right": {"total": 256, "increment": 109, "is_bonus": true, "bonus_message": ""}}],
    [1306, {"left": {"total": 461, "increment": 111, "is_bonus": true, "bonus_message": ""}, "right": {"total": 387, "increment": 131, "is_bonus": true, "bonus_message": ""}}],
    [1307, {"left": {"total": 605, "increment": 144, "is_bonus": true, "bonus_message": ""}, "right": {"total": 557, "increment": 170, "is_bonus": true, "bonus_message": ""}}],
    [1308, {"left": {"total": 813, "increment": 208, "is_bonus": true, "bonus_message": ""}, "right": {"total": 781, "increment": 224, "is_bonus": true, "bonus_message": ""}}],
    [1309, {"left": {"total": 1101, "increment": 288, "is_bonus": true, "bonus_message": ""}, "right": {"total": 1077, "increment": 296, "is_bonus": true, "bonus_message": ""}}],
    [1310, {"left": {"total": 1488, "increment": 387, "is_bonus": true, "bonus_message": ""}, "right": {"total": 1098, "increment": 21, "is_bonus": false, "bonus_message": ""}}],
    [1311, {"left": {"total": 1882, "increment": 394, "is_bonus": true, "bonus_message": ""}, "right": {"total": 1114, "increment": 16, "is_bonus": false, "bonus_message": ""}}],
    [1312, {"left": {"total": 1908, "increment": 26, "is_bonus": false, "bonus_message": ""}, "right": {"total": 1132, "increment": 18, "is_bonus": false, "bonus_message": ""}}],
    [1313, {"left": {"total": 1934, "increment": 26, "is_bonus": false, "bonus_message": ""}, "right": {"total": 1141, "increment": 9, "is_bonus": false, "bonus_message": ""}}],
    [1314, {"left": {"total": 1964, "increment": 30, "is_bonus": false, "bonus_message": ""}, "right": {"total": 1146, "increment": 5, "is_bonus": false, "bonus_message": ""}}],
    [1315, {"left": {"total": 1998, "increment": 34, "is_bonus": false, "bonus_message": ""}, "right": {"total": 1153, "increment": 7, "is_bonus": false, "bonus_message": ""}}],
    [1316, {"left": {"total": 2420, "increment": 422, "is_bonus": true, "bonus_message": "ay-caramba"}, "right": {"total": 1167, "increment": 14, "is_bonus": false, "bonus_message": ""}}],
    [1317, {"left": {"total": 2452, "increment": 32, "is_bonus": false, "bonus_message": ""}, "right": {"total": 1176, "increment": 9, "is_bonus": false, "bonus_message": ""}}],
    [1319, {"left": {"total": 2487, "increment": 35, "is_bonus": false, "bonus_message": ""}, "right": {"total": 1185, "increment": 9, "is_bonus": false, "bonus_message": ""}}],
    [1322, {"left": {"total": 2944, "increment": 457, "is_bonus": true, "bonus_message": ""}, "right": {"total": 2078, "increment": 893, "is_bonus": true, "bonus_message": "soy-la-leche"}}],
    [1322, {"left": {"total": 2968, "increment": 24, "is_bonus": false, "bonus_message": ""}, "right": {"total": 2102, "increment": 24, "is_bonus": false, "bonus_message": ""}}],
    [1323, {"left": {"total": 2999, "increment": 31, "is_bonus": false, "bonus_message": ""}, "right": {"total": 2116, "increment": 14, "is_bonus": false, "bonus_message": ""}}],
    [1326, {"left": {"total": 3026, "increment": 27, "is_bonus": false, "bonus_message": ""}, "right": {"total": 2132, "increment": 16, "is_bonus": false, "bonus_message": ""}}],
    [1327, {"left": {"total": 3795, "increment": 769, "is_bonus": true, "bonus_message": ""}, "right": {"total": 3189, "increment": 1057, "is_bonus": true, "bonus_message": "que-chulo"}}],
    [1328, {"left": {"total": 3813, "increment": 18, "is_bonus": false, "bonus_message": ""}, "right": {"total": 3204, "increment": 15, "is_bonus": false, "bonus_message": ""}}],
    [1329, {"left": {"total": 3839, "increment": 26, "is_bonus": false, "bonus_message": ""}, "right": {"total": 3217, "increment": 13, "is_bonus": false, "bonus_message": ""}}],
    [1330, {"left": {"total": 3871, "increment": 32, "is_bonus": false, "bonus_message": ""}, "right": {"total": 3228, "increment": 11, "is_bonus": false, "bonus_message": ""}}],
    [1331, {"left": {"total": 3903, "increment": 32, "is_bonus": false, "bonus_message": ""}, "right": {"total": 3240, "increment": 12, "is_bonus": false, "bonus_message": ""}}],
    [1332, {"left": {"total": 3929, "increment": 26, "is_bonus": false, "bonus_message": ""}, "right": {"total": 3254, "increment": 14, "is_bonus": false, "bonus_message": ""}}],
    [1333, {"left": {"total": 3950, "increment": 21, "is_bonus": false, "bonus_message": ""}, "right": {"total": 3272, "increment": 18, "is_bonus": false, "bonus_message": ""}}],
    [1334, {"left": {"total": 3977, "increment": 27, "is_bonus": false, "bonus_message": ""}, "right": {"total": 3286, "increment": 14, "is_bonus": false, "bonus_message": ""}}],
    [1335, {"left": {"total": 4001, "increment": 24, "is_bonus": false, "bonus_message": ""}, "right": {"total": 3302, "increment": 16, "is_bonus": false, "bonus_message": ""}}],
    [1336, {"left": {"total": 4037, "increment": 36, "is_bonus": false, "bonus_message": ""}, "right": {"total": 3315, "increment": 13, "is_bonus": false, "bonus_message": ""}}],
    [1337, {"left": {"total": 4066, "increment": 29, "is_bonus": false, "bonus_message": ""}, "right": {"total": 3330, "increment": 15, "is_bonus": false, "bonus_message": ""}}],
    [1338, {"left": {"total": 4095, "increment": 29, "is_bonus": false, "bonus_message": ""}, "right": {"total": 3344, "increment": 14, "is_bonus": false, "bonus_message": ""}}],
    [1339, {"left": {"total": 4116, "increment": 21, "is_bonus": false, "bonus_message": ""}, "right": {"total": 3359, "increment": 15, "is_bonus": false, "bonus_message": ""}}],
    [1340, "LEFT WINS"],
    [1340, {"left_lucha_pose": "win"}],
    [1340, {"right_lucha_pose": "loose"}],
  ]
}


export default {
  name: 'app',
  components: {
    FontAwesome,
    LuchaChili,LuchoMucho,
    BonusBaloon,
    HpBar,
    ScoreIncrement,
    TextVLabel,
    TextBigMessage,
    Box: posed.div({
      pressable: true,
      init: { scale: 1 },
      press: { scale: ({active}) => active?1.2:1 },
    }),
    Curtain: posed.div({
      visible: { opacity: 1 },
      hidden: { opacity: 0 },
    }),
    PopMessage: posed.div({
      visible: {
        scale: 1,
        opacity: 2,
      },
      hidden: {
        scale: 1.5,
        opacity: 0,
        transition: {
          scale:{
            type: 'spring',
            stiffness: 100,
            damping: 1,
            restDelta: 0.1,
            restSpeed: 1
          },
          opacity: {
            duration: 3000,
          }
        }
      }
    }),
    PopBaloon: posed.div({
      visible: {
        scale: 1,
        opacity: 1,
        transition: {
          scale:{
            type: 'spring',
            stiffness: 100,
            damping: 1,
            restDelta: 0.1,
            restSpeed: 1
          }
        }
      },
      hidden: {
        scale: 0,
        opacity: 0,
      }
    }),
    LuchaEmoji: posed.div({
      normal: {
        scale: 1,
      },
      shake: {
        x: true, // We're not using `to` in the transition but want to animate x
        transition: ({ from, velocity }) => spring({
          from, velocity,
          stiffness: 1000,
          damping: 100
        })
      },
      win: {scale: 1.3},
      loose: {scale: 0.7},
      hidden: {scale: 0.0},
    }),
    PopScore: posed.div({
      visible: {
        scale: 1,
        opacity: 2,
      },
      hidden: {
        scale: 1.5,
        opacity: 0,
        transition: {
          opacity: {
            duration: 1000,
          }
        }
      }
    }),
  },
  mounted() {
    setInterval(function() {
        this.current_second += 1
        // console.log(this.current_position, log_data.messages[this.current_position])
        while(log_data.messages[this.current_position][0] == this.current_second) {
          this.respondToMessage(log_data.messages[this.current_position][1])
          this.current_position += 1
        }
        // this.current_position += 1
    }.bind(this), 1000)
  },
  data: function() {
    return {
      current_second: log_data.start_offset,
      current_position:0,
      left: {
        score_pcnt: 0.5,
        score_increment: 0,
        emoji: null,
      },
      right: {
        score_pcnt: 0.5,
        score_increment: 0,
        emoji: null,
      },
      score_message: '',
      leftShow: true,
      rightShow: true,
      leftClass:'',
      battle_started: false,
      emojis: {
        normal: 'happy',
        attack: 'attack',
        defence: 'afraid',
        win: 'happy',
        loose: 'afraid',
      },

      leftScoreShow: false,
      rightScoreShow: false,

      leftCurtainShow: false,
      rightCurtainShow: false,

      bigMessageShow: false,
      bigMessageText: '',

      buttonLeftActive: true,
      buttonRightActive: true,

      bonusBaloonSymbol: null,
      bonusBaloonShow: false,

      disabledTimeout: 250,

      leftLuchaPose: 'hidden',
      rightLuchaPose: 'hidden',
    }
  },
  methods: {
    updateScore(data){
      if (this.battle_started){
        let left_score = parseFloat(data.left.total) + 10;
        let right_score = parseFloat(data.right.total) + 10;

        if(left_score + right_score > 0){
          this.left.score_pcnt = left_score / (left_score + right_score);
          this.right.score_pcnt = 1 - this.left.score_pcnt;
        }

        this.left.score_increment = data.left.increment;
        this.right.score_increment = data.right.increment;

        this.left.is_bonus = data.left.is_bonus;
        this.right.is_bonus = data.right.is_bonus;

        if (this.left.score_increment > this.right.score_increment) {
          if (data.left.is_bonus) {
            this.bonusLeft(data.left.bonus_message)
          } else {
            this.left.emoji = 'attack';
            this.right.emoji = 'defence';
          }
        } else if (this.left.score_increment < this.right.score_increment) {
          if (data.right.is_bonus) {
            this.bonusRight(data.right.bonus_message)
          } else {
            this.right.emoji = 'attack';
            this.left.emoji = 'defence';
          }
        } else {
          this.right.emoji = 'normal';
          this.left.emoji = 'normal';
        }
      }
    },
    startBattle() {
      this.left = {
        score_pcnt: 0.5,
        score_increment: 0,
        emoji: 'normal',
      };
      this.right = {
        score_pcnt: 0.5,
        score_increment: 0,
        emoji: 'normal',
      };
      this.battle_started = true;
      this.leftCurtainShow = false;
      this.rightCurtainShow = false;
      this.showBattleStart();
    },
    stopBattle(message) {
      this.battle_started = false;
      if (message.data == 'left'){this.winLeft()}
      else if (message.data == 'right'){this.winRight()}
    },
    showBattleStart() {
      this.showBigMessage('BATTLE START')
    },
    showBigMessage(text) {
      this.bigMessageText = text
    },
    bonusLeft(label) {
      this.showBonusBaloon(label);
      this.left.emoji = 'win';
      this.right.emoji = 'loose';
    },
    bonusRight(label) {
      this.showBonusBaloon(label);
      this.left.emoji = 'loose';
      this.right.emoji = 'win';
    },
    winLeft(){
      this.showBigMessage('LEFT WINS');
      // this.rightCurtainShow = true;
      this.left.emoji = 'win';
      this.right.emoji = 'loose';
    },
    winRight(){
      this.showBigMessage('RIGHT WINS');
      // this.leftCurtainShow = true;
      this.left.emoji = 'loose';
      this.right.emoji = 'win';
    },
    showRandomBonusBaloon() {
      let symbols = ['andale', 'ay-caramba', 'el-impacto', 'que-chulo', 'soy-la-leche']
      let label = symbols[Math.floor(Math.random() * symbols.length)]
      this.showBonusBaloon(label)
    },
    showBonusBaloon(label) {
      if(!label){
        let symbols = ['andale', 'ay-caramba', 'el-impacto', 'que-chulo', 'soy-la-leche']
        label = symbols[Math.floor(Math.random() * symbols.length)]
      }
      this.bonusBaloonSymbol = label;
      this.bonusBaloonShow = true;
      setTimeout(() => {this.bonusBaloonShow = false;}, 1000)
    },
    respondToMessage(message){
      console.log(message)
      if(message == 'battle_start') {
        this.startBattle()
      } else if (typeof message === 'string' || message instanceof String) {
        this.showBigMessage(message)
      } else if("left_lucha_pose" in message) {
        this.leftLuchaPose = message.left_lucha_pose;
      } else if("right_lucha_pose" in message) {
        this.rightLuchaPose = message.right_lucha_pose;
      }else{
        this.updateScore(message)
      }
    },
  },
  computed: {
    variantScoreLeft: function() {
      if (this.left.is_bonus) {return 'info'}
      else {return 'light'}
    },
    variantScoreRight: function() {
      if (this.right.is_bonus) {return 'info'}
      else {return 'light'}
    }


  },
}
</script>
