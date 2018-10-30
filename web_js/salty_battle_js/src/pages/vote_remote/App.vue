<template>
  <div>
      <!-- <center> -->
      <center style="width=100%; margin:15px; display: block">

        <div style="width:85%">
            <div style="position:relative;width:100%;height:0;padding-bottom: 56.25%;overflow: hidden;">
              <div id='player-1' style="position:absolute; top:0; left:0; width:100%; height:100%; z-index:-99"></div>

              <div style="position:absolute; top:0; left:0; width:100%; height:100%; z-index:-50">
                <div style="height:30%"/>
                  <!-- <PopMessage :pose="bigMessageShow ? 'visible': 'hidden'">
                    <center><h1 class="display-4"><b-badge variant="light">{{bigMessageText}}</b-badge></h1></center>
                  </PopMessage> -->
                  <TextBigMessage style="width:100%" :label="bigMessageText" />
              </div>

              <div style="position:absolute; top:0; left:20%; width:60%; height:30%; z-index:-50">
                <PopBaloon :pose="bonusBaloonShow?'visible':'hidden'">
                  <BonusBaloon :symbol="bonusBaloonSymbol"/>
                </PopBaloon>
              </div>

              <div style="position:absolute; top:0; left:0; width:100%; height:100%; z-index:-60;">
                  <div class="d-flex justify-content-between" style="height:100%;width:100%">
                    <Curtain :pose="leftCurtainShow ? 'visible': 'hidden'" style="width:50%;height:100%;background-color:#000"/>
                    <Curtain :pose="rightCurtainShow ? 'visible': 'hidden'" style="width:50%;height:100%;background-color:#000"/>
                  </div>
              </div>

              <div style="position: absolute;top:0;left:0;width:100%; height:100%;">
                <div style="width:100%;height:10%;"><HpBar :left="left.score_pcnt" :right="right.score_pcnt"/></div>
                <div class="d-flex justify-content-between" style="height:15%;width:100%">
                  <div><ScoreIncrement style="height=100%;width:40%" :score="left.score_increment" ref="ref_score_incr_left"/></div>
                  <div><ScoreIncrement style="height=100%;width:40%;" :score="right.score_increment" ref="ref_score_incr_right"/></div>
                </div>
                <div style="height:25%"/>
                <div class="d-flex justify-content-between" style="height:45%;z-index:10">
                  <Box style="width:40%">
                    <b-button variant="outline-light" @click="publishLeft" :disabled="!buttonLeftActive" block style="height:100%">
                      <div style="width:100%">
                        <svg style="position:relative;display: inline-block;width:100%;height:100%;" viewBox="0 0 300 200">
                          <LuchoMucho :symbol="emojis[left.emoji]" width="250" x="20"/>
                          <TextVLabel x="-80" y="140" height="50" label="LEFT"/>
                        </svg>
                      </div>
                    </b-button>
                  </Box>
                  <Box style="width:40%">
                    <b-button variant="outline-light" @click="publishRight" :disabled="!buttonRightActive" block style="height:100%">
                      <div style="width:100%">
                        <svg style="position:relative;display: inline-block;width:100%;height:100%;" viewBox="0 0 300 200">
                          <LuchaChili :symbol="emojis[right.emoji]" width="250" x="20"/>
                          <TextVLabel x="100" y="140" height="50" label="RIGHT"/>
                        </svg>
                      </div>
                    </b-button>
                  </Box>
                </div>
              </div>

            </div>
            <b-button @click="unmute">Unmute</b-button>
            <!-- <b-button @click="showRandomBonusBaloon">Baloon</b-button>
            <b-button @click="randomScore">Score</b-button> -->
            <!-- <b-button @click="showBattleStart">battle</b-button>
            <b-button @click="showLeftScore">score</b-button>
            <b-button @click="rightCurtainShow = !rightCurtainShow;">curtain</b-button> -->
            <!-- <div style="width:100px"><LuchaChili symbol="afraid"/></div><br> -->
            <!-- <div style="width:100px"><LuchoMucho symbol="attack"/></div><br> -->
            <!-- <div style="width:500px"><LeftText/></div><br> -->
        </div>
      <!-- </center> -->
    </center>
  </div>
</template>

<script>
import * as Ably from 'ably';
import YouTubePlayer from 'youtube-player';
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
      press: { scale: 1.2 },
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
      rest: {
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
    })
  },
  created() {
      this.client = new Ably.Realtime('iu0Lmw.hC3rhw:MEeGgoGc7kI4xQa1');
      this.channel_votes = this.client.channels.get("votes");
      this.channel_stats = this.client.channels.get("stats");

      this.channel_stats.subscribe('score', this.updateScore);
      this.channel_stats.subscribe('start_video', this.startVideo);
      this.channel_stats.subscribe('stop_video', this.stopVideo);
      this.channel_stats.subscribe('start_battle', this.startBattle);
      this.channel_stats.subscribe('stop_battle', this.stopBattle);

  },
  mounted() {
    this.youtube_player = YouTubePlayer('player-1');
    this.youtube_player.mute();
  },
  data: function() {
    return {
      client: null,
      channel_votes: null,
      channel_stats: null,
      youtube_player: null,
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
    }
  },
  methods: {
    updateScore(message){
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
            this.bonusLeft()
          } else {
            this.left.emoji = 'attack';
            this.right.emoji = 'defence';
          }
        } else if (this.left.score_increment < this.right.score_increment) {
          if (data.right.is_bonus) {
            this.bonusRight()
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
    publishLeft(){
      this.channel_votes.publish("left", "1");
      this.buttonLeftActive = false;
      setTimeout(()=> {this.buttonLeftActive = true;}, 500)
    },
    publishRight(){
      this.channel_votes.publish("right", "1");
      this.buttonRightActive = false;
      setTimeout(()=> {this.buttonRightActive = true;}, 500)
    },
    startVideo(message) {
      let data = JSON.parse(message.data)
      this.youtube_player.loadVideoById(data.video_id, data.starts);
      setTimeout(() => {
        this.youtube_player.playVideo();
      }, 3000);
    },
    stopVideo() {
      this.youtube_player.pauseVideo();
    },
    startBattle(message) {
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
      console.log('STOP BATTLE')
      console.log(message)
      this.battle_started = false;
      if (message.data == 'left'){this.winLeft()}
      else if (message.data == 'right'){this.winRight()}
    },
    showBattleStart() {
      this.showBigMessage('BATTLE START')
    },
    unmute() {
      this.youtube_player.unMute();
    },
    showBigMessage(text) {
      this.bigMessageText = text
    },
    bonusLeft() {
      this.showRandomBonusBaloon();
      this.left.emoji = 'win';
      this.right.emoji = 'loose';
    },
    bonusRight() {
      this.showRandomBonusBaloon();
      this.left.emoji = 'loose';
      this.right.emoji = 'win';
    },
    winLeft(){
      this.showBigMessage('LEFT WINS');
      this.rightCurtainShow = true;
      this.left.emoji = 'win';
      this.right.emoji = 'loose';
    },
    winRight(){
      this.showBigMessage('RIGHT WINS');
      this.leftCurtainShow = true;
      this.left.emoji = 'loose';
      this.right.emoji = 'win';
    },
    showRandomBonusBaloon() {
      let symbols = ['andale', 'ay-caramba', 'el-impacto', 'que-chulo', 'soy-la-leche']
      let s = symbols[Math.floor(Math.random() * symbols.length)]
      console.log(s)
      this.bonusBaloonSymbol = s;
      this.bonusBaloonShow = true;
      setTimeout(() => {this.bonusBaloonShow = false;}, 1000)
    },
    randomScore() {
      let score = Math.random();
      this.left.score_pcnt = score;
      this.right.score_pcnt = 1 - score;
      console.log(score)
      this.$refs.ref_score_incr_left.showScore();
      this.$refs.ref_score_incr_right.showScore();
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
