<template>
  <div>
      <!-- <center> -->
      <center style="width=100%; margin:15px; display: block">

        <div style="width:85%">
            <div style="position:relative;width:100%;height:0;padding-bottom: 56.25%;overflow: hidden;">
              <div id='player-1' style="position:absolute; top:0; left:0; width:100%; height:100%; z-index:-99"></div>

              <div style="position:absolute; top:0; left:0; width:100%; height:100%; z-index:-50">
                <div style="height:30%"/>
                  <PopMessage :pose="bigMessageShow ? 'visible': 'hidden'">
                    <center><h1 class="display-4"><b-badge variant="light">{{bigMessageText}}</b-badge></h1></center>
                  </PopMessage>
              </div>

              <div style="position:absolute; top:0; left:0; width:100%; height:100%; z-index:-50;">
                <div style="height:15%"/>
                <center>
                  <div class="d-flex justify-content-between" style="height:35%;width:90%;">
                    <PopScore :pose="leftScoreShow ? 'visible': 'hidden'"><h1><b-badge :variant="variantScoreLeft">+{{left.score_increment}}</b-badge></h1></PopScore>
                    <PopScore :pose="rightScoreShow ? 'visible': 'hidden'"><h1><b-badge :variant="variantScoreRight">+{{right.score_increment}}</b-badge></h1></PopScore>
                  </div>
                </center>
              </div>

              <div style="position:absolute; top:0; left:0; width:100%; height:100%; z-index:-60;">
                  <div class="d-flex justify-content-between" style="height:100%;width:100%">
                    <Curtain :pose="leftCurtainShow ? 'visible': 'hidden'" style="width:50%;height:100%;background-color:#000"/>
                    <Curtain :pose="rightCurtainShow ? 'visible': 'hidden'" style="width:50%;height:100%;background-color:#000"/>
                  </div>
              </div>

              <div style="position: absolute;top:0;left:0;width:100%; height:100%;">
                <b-progress class="mt-2" :max="1" animated height="10%" style="margin-bottom:5%">
                  <b-progress-bar :value="left.score_pcnt" variant="info"></b-progress-bar>
                  <b-progress-bar :value="right.score_pcnt" variant="secondary"></b-progress-bar>
                </b-progress>
                <div style="height:40%"/>
                <div class="d-flex justify-content-between" style="height:35%;z-index:10">
                  <Box style="width:35%">
                    <b-button variant="outline-light" @click="publishLeft" :disabled="!buttonLeftActive" block style="height:100%">
                      <center>
                      <i class="far display-4" v-bind:class="'fa-'+emojis[left.emoji]"/><br>
                      LEFT
                    </center>
                    </b-button>
                  </Box>
                  <Box style="width:35%">
                    <b-button variant="outline-light" @click="publishRight" :disabled="!buttonRightActive" block style="height:100%">
                      <center>
                      <i class="far display-4" v-bind:class="'fa-'+emojis[right.emoji]"/><br>
                      RIGHT
                    </center>
                    </b-button>
                  </Box>
                </div>
              </div>

            </div>
            <b-button @click="unmute">Unmute</b-button>
            <!-- <b-button @click="showBattleStart">battle</b-button>
            <b-button @click="showLeftScore">score</b-button>
            <b-button @click="rightCurtainShow = !rightCurtainShow;">curtain</b-button> -->
        </div>
      <!-- </center> -->
    </center>
  </div>
</template>

<script>
import * as Ably from 'ably';
import YouTubePlayer from 'youtube-player';
import FontAwesome from '../../components/FontAwesome.vue';
import posed, { PoseTransition } from "vue-pose";
export default {
  name: 'app',
  components: {
    FontAwesome,
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
        emoji: 'normal',
      },
      right: {
        score_pcnt: 0.5,
        score_increment: 0,
        emoji: 'normal',
      },
      score_message: '',
      leftShow: true,
      rightShow: true,
      leftClass:'',
      battle_started: false,
      emojis: {
        normal: 'laugh-squint',
        attack: 'grin-tongue-squint',
        defence: 'tired',
        win: 'grin-stars',
        loose: 'dizzy',
      },

      leftScoreShow: false,
      rightScoreShow: false,

      leftCurtainShow: false,
      rightCurtainShow: false,

      bigMessageShow: false,
      bigMessageText: '',

      buttonLeftActive: true,
      buttonRightActive: true,
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

        if(this.left.score_increment > 0) {this.showLeftScore()}
        if(this.right.score_increment > 0) {this.showRightScore()}

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
      this.bigMessageShow = true;
      setTimeout(() => {this.bigMessageShow = false;}, 100)
    },
    showLeftScore() {
      this.leftScoreShow = true;
      setTimeout(() => {this.leftScoreShow = false;}, 500)
    },
    showRightScore() {
      this.rightScoreShow = true;
      setTimeout(() => {this.rightScoreShow = false;}, 500)
    },
    bonusLeft() {
      this.showBigMessage('AY CARAMBA');
      this.left.emoji = 'win';
      this.right.emoji = 'loose';
    },
    bonusRight() {
      this.showBigMessage('AY CARAMBA');
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
