<template>
	<div class="pre-loader">
		<div class="pre-loader__container">
			<div class="logo-continer">
				<img src="preloader.svg" alt="">
			</div>
			<div class="text">Loading<span>{{dots}}</span></div>
		</div>
	</div>
</template>
<script>
	export default {
		data(){
			return {
				dots: '.',
			}
		},
		created(){
			 
			let i = 0;
			setInterval(() => {
				if (i != 2) {
					i++
					this.dots = this.dots + '.'
				}else{ 
					i = 0;
					this.dots = '.'
				}
			}, 600)
		}
	}
</script>
<style lang="scss">
	@keyframes rotate{
		0%{
			transform: rotate(0deg);
		}
		100%{
			transform: rotate(360deg);
		}
	}
	.pre-loader{
		position: absolute;
		top: 0;
		left: 0;
		background: rgba(0,0,0,0.5);
		width: 100vw;
		height: 100vh;
		z-index: 5;
		color: #fff;

	}
	.logo-continer{
		width: 90px;
		height: 90px;
		background: #242323;
		margin-bottom: 10px;
		display: flex;
		justify-content: center;
		align-items: center;
	}
	.pre-loader__container{
		position: absolute;
		top: 50%;
		left: 50%;
		transform: translate(-50%, -50%);
		img{
			width: 64px;
			animation: rotate 3s cubic-bezier(0.29, 0.9, 0.39, 0.93) infinite;
		}
		.text{
			width: 100px;
		}

	}
</style>