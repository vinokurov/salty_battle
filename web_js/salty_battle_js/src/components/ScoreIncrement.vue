<template>
<svg role="img" viewBox="0 0 100 100">
  <text x="0" y="50" :transform="'scale('+scale+')'" :opacity="opacity" style="fill:black; stroke:white;">
    +{{scoreLabel}}
  </text>
</svg>
</template>

<script>
import { tween, spring } from 'popmotion';
export default{
  props:['score'],
  data:function() {
    return {
      currentAction:null,
      x:20,
      y:20,
      scale:0,
      opacity:0,
      scoreLabel:0,
    }
  },
  methods:{
    showScore: function() {
      if(this.score > 0) {
        if(this.currentAction){this.currentAction.stop()}
        this.currentAction = spring({
          from:{scale:0,opacity:0},
          to:{scale:1, opacity:1},
          stiffness:{scale:500, opacity:1000}}).start({
            update: v => {
              this.scale = v.scale;
              this.opacity = v.opacity;
            },
            complete: this.hideScore
          })
      }
    },
    hideScore: function() {
      if(this.currentAction){this.currentAction.stop()}
      let currentOpacity = this.opacity;
      let currentScale = this.scale;
      this.currentAction = tween({
        from:{o:currentOpacity,s:currentScale},
        to: {o:0,s:0},
        duration:50
      }).start(v => {this.opacity=v.o;this.scale=v.s;})
    }
  },
  watch: {
    score: function() {
      if(this.score>0)
      {
        this.hideScore();
        this.scoreLabel = this.score;
        this.showScore()
      }
    }
  },
}
</script>

<style scoped>
@font-face {
		font-family: 'BadaboomBB';
		src: url('https://s3-us-west-2.amazonaws.com/s.cdpn.io/4273/badaboombb.woff2') format('woff2'),
		url('https://s3-us-west-2.amazonaws.com/s.cdpn.io/4273/badaboombb.woff') format('woff');
		font-style: normal;
		font-weight: 400;
		}
text {
			font-size: 40px;
			font-family: BadaboomBB, script;
}
/* section:last-of-type svg text {
  filter: url(#shadow);
  fill: url(#hexapolka);
} */
</style>
