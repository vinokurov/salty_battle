<template>
  <svg role="img" viewBox="0 0 200 50">
    <text x="100" y="20" text-anchor="middle" :transform="'scale('+scale+')'" :opacity="opacity" style="fill:black; stroke:white;">
      {{label}}
    </text>
  </svg>
</template>

<script>
import { tween, spring } from 'popmotion';
export default {
  props:['label'],
  data: function() {
    return {
      labelText:null,
      currentAction:null,
      opacity:0,
      scale:0,
    }
  },
  methods:{
    showMessage: function() {
      if(this.currentAction){this.currentAction.stop()}
      this.currentAction = spring({
        from:{scale:0,opacity:0},
        to:{scale:1, opacity:1},
        stiffness:{scale:500, opacity:1000}}).start({
          update: v => {
            this.scale = v.scale;
            this.opacity = v.opacity;
          },
          complete: this.hideMessage
      })
    },
    hideMessage: function() {
      if(this.currentAction){this.currentAction.stop()}
      let currentOpacity = this.opacity;
      let currentScale = this.scale;
      this.currentAction = tween({
        from:{o:currentOpacity,s:currentScale},
        to: {o:0,s:0},
        duration:500
      }).start(v => {this.opacity=v.o;this.scale=v.s;})
    }
  },
  watch:{
    label: function() {
      this.labelText = this.label;
      this.showMessage();
    }
  }
}
</script>
<style scoped>
@font-face {
		font-family: 'BadaboomBB';
		src: url('https://s3-us-west-2.amazonaws.com/s.cdpn.io/4273/badaboombb.woff2') format('woff2'),
		url('https://s3-us-west-2.amazonaws.com/s.cdpn.io/4273/badaboombb.woff') format('woff');
		font-style: normal;
		/* font-weight: 400; */
		font-weight: 400;
		}
text {
			/* font-size: 20px; */
			font-size: 20px;
			font-family: BadaboomBB, script;
      text-align:center;
      background-color: #555;
}
</style>
