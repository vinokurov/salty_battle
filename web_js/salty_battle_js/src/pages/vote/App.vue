<template>
  <div style="position:absolute;height:90%;width:100%;overflow: hidden;">
    <div class="d-flex justify-content-between" style="height:100%">
      <Box style="width:49%;height:100%" v-bind:active="buttonLeftActive">
        <b-button variant="info" @click="publishLeft" :disabled="!buttonLeftActive" block style="height:100%">
          <h1>LEFT</h1>
        </b-button>
      </Box>
      <Box style="width:49%;height:100%" v-bind:active="buttonRightActive">
        <b-button variant="info" @click="publishRight" :disabled="!buttonRightActive" block style="height:100%">
          <h1>RIGHT</h1>
        </b-button>
      </Box>
    </div>
  </div>
</template>

<script>
import * as Ably from 'ably';
import FontAwesome from '../../components/FontAwesome.vue';
import posed, { PoseTransition } from "vue-pose";
export default {
  name: 'app',
  components: {
    FontAwesome,
    Box: posed.div({
      pressable: true,
      init: { scale: 1 },
      press: { scale: ({active}) => active?1.2:1 },
    }),
  },
  created() {
      this.client = new Ably.Realtime('iu0Lmw.hC3rhw:MEeGgoGc7kI4xQa1');
      // this.channel_votes = this.client.channels.get("votes");
      this.channel_votes_left = this.client.channels.get("votes_left");
      this.channel_votes_right = this.client.channels.get("votes_right");

      this.channel_stats = this.client.channels.get("stats");
      this.channel_stats.subscribe('disabled_timeout', this.updateDisabledTimeout);
  },
  data: function() {
    return {
        client: null,
        channel_control: null,
        channel_stats: null,

        contestants: [],
        battleName: '',
        contestantLeft: '',
        contestantRight: '',

        buttonLeftActive: true,
        buttonRightActive: true,

        disabledTimeout: 250,
    }
  },
  methods: {
    publishLeft() {
      this.channel_votes_left.publish("vote", "1");
      this.buttonLeftActive = false;
      setTimeout(()=> {this.buttonLeftActive = true;}, this.disabledTimeout)
    },
    publishRight() {
      this.channel_votes_right.publish("vote", "1");
      this.buttonRightActive = false;
      setTimeout(()=> {this.buttonRightActive = true;}, this.disabledTimeout)
    },
    updateDisabledTimeout(message) {
      this.disabledTimeout = parseInt(message.data)
    },
  }
}
</script>
