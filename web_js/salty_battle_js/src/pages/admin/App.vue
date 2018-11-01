<template>
  <div class="container">
    <br/>
    <b-card>
      <h2>Battle</h2>
      <b-button @click="battleStart">START</b-button>
      <b-button @click="battleStop">STOP</b-button>
    </b-card>
    <br/>
    <b-card>
      <h2>Video</h2>
      <b-form inline>
        <b-input placeholder="Video ID" v-model="youtubeVideoID"/>
        <b-input placeholder="Starts"  v-model="youtubeVideoStart"/>
      </b-form>
      <b-button @click="videoStart">START</b-button>
      <b-button @click="videoStop">STOP</b-button>
      <br/>
      <br/>
      <!-- <b-button size="sm" @click="getVideoId(video)" v-for="d,video in videos">{{video}}</b-button> -->
    </b-card>
    <br/>

    <b-card>
      <h2>Control</h2>
      <b-input-group prepend="Timeout, ms" size="sm" >
        <b-form-input v-model="controlTimeout"></b-form-input>
        <b-input-group-append><b-btn @click="controlTimeoutPublish">Publish</b-btn></b-input-group-append>
      </b-input-group>
      <br/>

      <b-input-group prepend="Bonus Z Threshold" size="sm" >
        <b-form-input v-model="controlBonusThreshold"></b-form-input>
        <b-input-group-append><b-btn @click="controlBonusThresholdPublish">Publish</b-btn></b-input-group-append>
      </b-input-group>
      <br/>

      <!-- <b-button size="sm" @click="getVideoId(video)" v-for="d,video in videos">{{video}}</b-button> -->
    </b-card>
    <br/>



    <b-card>
      <h2>Stat Details</h2>
      <b-table striped hover small :items="statDetailsData"
        :fields="['l_total', 'l_val', 'l_mean', 'l_std', 'l_z', 'r_total', 'r_val', 'r_mean', 'r_std', 'r_z',]"/>
    </b-card>

  </div>
</template>

<script>
import * as Ably from 'ably';
import FontAwesome from '../../components/FontAwesome.vue'
export default {
  name: 'app',
  components: {FontAwesome},
  created() {
      this.client = new Ably.Realtime('iu0Lmw.hC3rhw:MEeGgoGc7kI4xQa1');
      this.channel_control = this.client.channels.get("control");
      this.channel_stats = this.client.channels.get("stats");

      this.channel_stats.subscribe('stats_details', this.updateStatsDetails);
  },
  data: function() {
    return {
        client: null,
        channel_control: null,

        contestants: [],
        battleName: '',
        contestantLeft: '',
        contestantRight: '',

        youtubeVideoID: '',
        youtubeVideoStart: null,

        videoStarted: false,
        videoTimer: null,

        videos: {
          'ghx2017': {id: 'cxcQDH-nmxs', t:358},
          'rtsf2018': {id:'cJxHADoRRMs', t: 86},
          'lindyfest2018': {id:'Jgtu9s-GNkg', t: 416},
          'savoy-1': {id:'b7wsVZnCIms', t: 5},
          'savoy-2': {id:'H4KJp2WQbG4', t: 5},
          'savoy-3': {id:'59bQ5Vw0YcE', t: 5},
          'savoy-4': {id:'w50fREdubFU', t: 5},
          'savoy-5': {id:'rnMBqEiirTo', t: 5},
        },

        statDetailsData: [],

        controlTimeout: 250,
        controlBonusThreshold: 2.0,
    }
  },
  methods: {
    battleStart() {
      this.channel_control.publish("start_battle", "");
    },
    battleStop() {
      this.channel_control.publish("stop_battle", "");
    },
    videoStart() {
      let message = {video_id: this.youtubeVideoID, starts: this.youtubeVideoStart}
      this.channel_stats.publish("start_video", JSON.stringify(message))
      this.startVideoTimer();
    },
    videoStop() {
      this.stopVideoTimer();
      this.channel_stats.publish("stop_video", "")
    },
    startVideoTimer() {
      this.videoTimer = setInterval(function() {
          console.log('resending')
          let message = {video_id: this.youtubeVideoID, starts: this.youtubeVideoStart}
          this.channel_stats.publish("start_video", JSON.stringify(message))
      }.bind(this), 60*1000)
    },
    stopVideoTimer() {
      clearInterval(this.videoTimer);
    },
    getVideoId(key){
      let video = this.videos[key];
      this.youtubeVideoID = video.id;
      this.youtubeVideoStart = video.t;

    },
    updateStatsDetails(message){
      console.log(message.data)
      // let data = JSON.parse(message.data);
      if(this.statDetailsData.length > 60){this.statDetailsData.pop()}
      this.statDetailsData.unshift(message.data)
    },
    controlTimeoutPublish(){
      this.channel_stats.publish('disabled_timeout', this.controlTimeout)
    },
    controlBonusThresholdPublish(){
      this.channel_control.publish('bonus_z_threshold', this.controlBonusThreshold)
    }
  }
}
</script>
