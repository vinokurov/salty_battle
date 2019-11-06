<template>
  <div>
      <!-- <center> -->
      <center style="width:100%; margin:0px; display: block">

        <div :style="'width:100%'">
            <div style="position:relative;width:100%;height:0;padding-bottom: 56.25%;overflow: hidden;">

              <div style="position:absolute; top:0; left:0; width:100%; height:100%; z-index:0">
                <div style="height:30%"/>
                  <TextBigMessage style="width:100%" :label="bigMessageText" />
              </div>

              <!-- <div style="position:absolute; top:10%; left:20%; width:60%; height:30%; z-index:50;text-color:black">{{current_second}}</div> -->

              <!-- <div style="position:absolute; top:70%; left:40%; width:20%; height:10%; z-index:50"> -->
              <div style="position:absolute; top:0; left:20%; width:60%; height:30%; z-index:-50">
                <PopBaloon :pose="bonusBaloonShow?'visible':'hidden'">
                  <BonusBaloon :symbol="bonusBaloonSymbol"/>
                </PopBaloon>
              </div>

              <div style="position: absolute;top:20%;left:0%;width:100%;height:5%;z-index:-100">
                <img width="50%" src="salty_battle.jpg"/>
              </div>
              
              <div style="position: absolute;top:5%;left:0%;width:100%;height:5%;z-index:-100">
                <!-- <h2 class="text-white">https://www.saltyjitterbugs.co.uk</h2> -->
                <img width="50%" src="url.png"/>
              </div>

              <div style="position: absolute;top:80%;left:10%;width:80%;height:5%;"></div>

              <div style="position: absolute;top:70%;left:10%;width:80%;height:5%;">
                <HpBar :left="left.score_pcnt" :right="right.score_pcnt"/>
              </div>

              <div style="position: absolute;top:70%;left:12%;width:78%; height:15%;">
                <div class="d-flex justify-content-between" style="height:100%;width:100%">
                  <div><ScoreIncrement style="height=100%;width:40%" :score="left.score_increment" ref="ref_score_incr_left"/></div>
                  <div><ScoreIncrement style="height=100%;width:40%;" :score="right.score_increment" ref="ref_score_incr_right"/></div>
                </div>
              </div>

              <div style="position: absolute;top:70%;left:0;width:100%; height:20%;">
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
            <!-- <b-button @click="showRandomBonusBaloon">Baloon</b-button> -->

        </div>
      <!-- </center> -->
    </center>
  </div>
</template>

<script>
import * as Ably from 'ably';
import FontAwesome from '../../components/FontAwesome.vue';
import LuchaChili from '../../components/LuchaChili.vue';
import LuchoMucho from '../../components/LuchoMucho.vue';
import BonusBaloon from '../../components/BonusBaloon.vue';
import HpBar from '../../components/HpBar.vue';
import ScoreIncrement from '../../components/ScoreIncrement.vue';
import TextVLabel from '../../components/TextVLabel.vue';
import TextBigMessage from '../../components/TextBigMessage.vue';
import posed, { PoseTransition } from "vue-pose";


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
  created() {
      console.log('Starting')
      this.client = new Ably.Realtime('iu0Lmw.hC3rhw:MEeGgoGc7kI4xQa1');

      this.channel_stats = this.client.channels.get("stats");

      this.channel_stats.subscribe('score', this.updateScore);
      this.channel_stats.subscribe('start_battle', this.startBattle);
      this.channel_stats.subscribe('stop_battle', this.stopBattle);

  },

  data: function() {
    return {
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

      leftLuchaPose: 'normal',
      rightLuchaPose: 'normal',
    }
  },
  methods: {
    updateScore(message){
      console.log(message)
      if (this.battle_started){
        this.score_message = message.data
        let data = JSON.parse(message.data)
        
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
      this.leftLuchaPose = 'normal'
      this.rightLuchaPose = 'normal'
    },
    stopBattle(message) {
      this.battle_started = false;
      if (message.data == 'left'){this.winLeft()}
      else if (message.data == 'right'){this.winRight()}
      this.leftLuchaPose = 'hiden'
      this.rightLuchaPose = 'hidden'
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
