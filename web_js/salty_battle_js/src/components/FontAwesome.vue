<template>
	<i v-bind:class="classes" aria-hidden="true"></i>
</template>

<script>
export default {
  name: 'FontAwesome',
  props: {
  	    icon: String
  	},
  	computed: {
	    classes: function () {
				return ['fa', 'fa-fw', 'fa-' + this.icon]
			}
  }
}
</script>
