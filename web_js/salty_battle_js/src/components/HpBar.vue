<template>
  <svg role="presentation" viewBox="0 0 250 30">
    <polygon :points="'125,10 '+leftBar_left+',10 '+leftBar_left+',25, 125,25'" style="fill:#DBC609;stroke:white;stroke-width:2;fill-opacity:1;stroke-opacity:1" />
    <polygon :points="'125,10 '+rightBar_right+',10 '+rightBar_right+',25, 125,25'" style="fill:#FF06AC;stroke:white;stroke-width:2;fill-opacity:1;stroke-opacity:1" />
    <rect x="124" y="5" height="25" width="2" style="fill:white;stroke:white;" />
  </svg>
</template>

<script>
import { tween, spring } from 'popmotion';
export default{
  props: ['left', 'right'],
  data: function() {
    return {
      leftBar_left:125,
      rightBar_right:125,
      leftTween: null,
      rightTween: null,
    }
  },
  watch:{
    left: function() {
      let score = Math.floor(this.left*100)
      let from = this.leftBar_left;
      if (this.leftTween){this.leftTween.stop()}
      if (score > 50){
        let to = 125 - (score-50)*2;
        this.leftTween = spring({from:from, to:to, stiffness:500}).start(v => {this.leftBar_left = v});
      } else{
        this.leftTween = tween({from:from, to:125, duration:100}).start(v => {this.leftBar_left = v});
      }
    },
    right: function() {
      let score = Math.floor(this.right*100)
      let from = this.rightBar_right;
      if (this.rightTween){this.rightTween.stop()}
      if (score > 50){
        let to = 125 + (score-50)*2;
        this.rightTween = spring({from:from, to:to, stiffness:500}).start(v => {this.rightBar_right = v});
      } else{
        this.rightTween = tween({from:from, to:125, duration:100}).start(v => {this.rightBar_right = v});
      }
    }
  },
}
</script>
