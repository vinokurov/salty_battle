<template>
  <svg role="img" viewBox="0 0 50 22">
    <text x="0" y="20" style="fill:black; stroke:white;">
      {{label}}
    </text>
  </svg>
</template>

<script>
export default {props:['label']}
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
			font-size: 20px;
			font-family: BadaboomBB, script;
      text-align:center;
      background-color: #555;
      /* writing-mode: tb; */
      /* glyph-orientation-vertical: 0; */
}
</style>
