<template>
  <div style="height=100%">
    <div class="d-flex justify-content-between" style="height:100%">
      <Box style="width:49%;height=100%"><b-button variant="info" @click="publishLeft" :disabled="!buttonLeftActive" block><h1>LEFT</h1></b-button></box>
      <Box style="width:49%;height=100%"><b-button variant="info" @click="publishRight" :disabled="!buttonRightActive" block><h1>RIGHT</h1></b-button></Box>
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
      press: { scale: 1.2 },
    }),
  },
  created() {
      this.client = new Ably.Realtime('iu0Lmw.hC3rhw:MEeGgoGc7kI4xQa1');
      this.channel_votes = this.client.channels.get("votes");
  },
  data: function() {
    return {
        client: null,
        channel_control: null,

        contestants: [],
        battleName: '',
        contestantLeft: '',
        contestantRight: '',

        buttonLeftActive: true,
        buttonRightActive: true,
    }
  },
  methods: {
    publishLeft() {
      this.channel_votes.publish("left", "1");
      this.buttonLeftActive = false;
      setTimeout(()=> {this.buttonLeftActive = true;}, 500)
    },
    publishRight() {
      this.channel_votes.publish("right", "1");
      this.buttonRightActive = false;
      setTimeout(()=> {this.buttonRightActive = true;}, 500)
    }
  }
}
</script>
