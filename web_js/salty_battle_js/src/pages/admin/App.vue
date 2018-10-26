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
      <b-button size="sm" @click="getVideoId(video)" v-for="d,video in videos">{{video}}</b-button>
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

        videos: {
          'ghx2017': {id: 'cxcQDH-nmxs', t:358},
          'rtsf2018': {id:'cJxHADoRRMs', t: 86},
          'lindyfest2018': {id:'Jgtu9s-GNkg', t: 416},
          'savoy-1': {id:'b7wsVZnCIms', t: 5},
          'savoy-2': {id:'H4KJp2WQbG4', t: 5},
          'savoy-3': {id:'59bQ5Vw0YcE', t: 5},
          'savoy-4': {id:'w50fREdubFU', t: 5},
          'savoy-5': {id:'rnMBqEiirTo', t: 5},
        }
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
    },
    videoStop() {
      this.channel_stats.publish("stop_video", "")
    },
    getVideoId(key){
      let video = this.videos[key];
      this.youtubeVideoID = video.id;
      this.youtubeVideoStart = video.t;

    },
  }
}
</script>
