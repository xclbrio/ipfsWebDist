<template>
	<div class="alert">
		<header class="alert-header">
			<h3 :class="ctx" class="alert-title">{{title}}</h3>
			<div @click="$emit('close')" class="close-btn">
				<svg width="10" height="10" xmlns="http://www.w3.org/2000/svg" version="1.1" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 10 10">
					<g transform="matrix(1,0,0,1,-351,-64)">
						<path d="M352,72.07107l3.18198,-3.18198l-3.18198,-3.18198l0.7071,-0.70711l3.18198,3.18198l3.18198,-3.18198l0.7071,0.70711l-3.18198,3.18198l3.18198,3.18198l-0.70711,0.7071l-3.18197,-3.18198l-3.18198,3.18198z" fill-opacity="0" fill="#ffffff" stroke-linejoin="miter" stroke-linecap="butt" stroke-opacity="1" stroke="#ffffff" stroke-miterlimit="50" stroke-width="1" id="Path-0"/>
					</g>
				</svg>
			</div>
		</header>
		<div class="alert-body">
			<slot></slot>
		</div>
	</div>
</template>
<script>
	export default{
		props: {
			ctx: {
				type: String,
				default: ''
			},
			title: {
				type: String,
				default: ''
			},

		}
	}
</script>
<style lang="scss">
	@import '../_base.scss';
	.alert{
		position: absolute;
		top: 50%;
		left: 50%;
		transform: translate(-50%, -50%);
		width: 680px;
		max-width: 95vw;
		background-color: $black-three;
		padding: 5px;
		z-index: 5;
		box-shadow: 0px 2px 2px rgba(0, 0, 0, 0.5);
 		color: $white;
		.close-btn{
			padding: 0;
		}
	}
	.alert-header{
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin: 7px 14px 13px;
		font-size: 17px;
	}
	.close-btn{
		cursor: pointer;
	}
	.alert-title{
		font-size: 17px;
		margin: 0;
		&.error{
			color: #ff5e57;
		}

		&.transaction{
			color: #ffffff;
		}
	}
	.alert-body{
		background-color: #2c2c2c;
		padding: 39px 50px;
	}

</style>