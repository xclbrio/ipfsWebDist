<template>
	<div class="chart">
		<div class="chart__container">
			<div class="meta">
				<div>
					<!-- <button @click="stockOptions.xAxis.range += 3600 * 1000">selected</button> -->
					<div>{{new Date(date).toUTCString().substr(0, 11).toUpperCase()}}, VOLUME: {{volumeLegend}}</div>
					<div><span class="greyish">OP: </span>{{open}}, <span class="greyish">HI: </span>{{high}}, <span class="greyish">LW: </span>{{low}}, <span class="greyish">CL: </span>{{close}}</div>
				</div>
			</div>
			<highcharts id="chart" ref="chart" class="stock" :constructor-type="'stockChart'" :options="stockOptions"></highcharts>
		</div>
	</div>
</template>

<script>
	import settings from '../settings.json'
	export default{
		name: 'chart',
		data(){
			return{
				chartData: [],
				date: '',
				close: '',
				open: '',
				high: '',
				low: '',
				volumeLegend: '',
				range: [43200000, 172800000, 5184000000],
				rangeCheker: true,
				intervalIsActive: true,
				dataGrouping: [{
					forced: true,
					units: [['minute', [15]]]
				},
				{
					forced: true,
					units: [['hour', [1]]]
				},
				{
					forced: true,
					units: [['day', [1]]]
				}],
				stockOptions: {
					chart: {
						style: {
							fontFamily: "\"Roboto Mono \", monospace",
							fontSize: "12px",
							fontWeight: "bold"
						},
						height: "50%",
						panning: true,
						pinchType: 'x',
						zoomType: false,
					},
					plotOptions: {
						series: {
							dataGrouping: this.dataGrouping,
							forced: true,
						}
					},
					updateArgs: [true, true, { duration: 1000 }],
					rangeSelector: {
						inputEnabled: false,
						allButtonsEnabled: true,
						buttonPosition: {
							align: 'right'
						},
						buttons: [{
							type: 'hour',
							count: 6,
							text: '15M',
							preserveDataGrouping: true,
							dataGrouping: {
								forced: true,
								units: [['minute', [15]]]
							}
						}, {
							type: 'hour',
							count: 24,
							text: '1H',
							preserveDataGrouping: true,
							dataGrouping: {
								forced: true,
								units: [['hour', [1]]]
							}
						}, {
							type: 'day',
							count: 24,
							text: '1D',
							preserveDataGrouping: true,
							dataGrouping: {
								forced: true,
								units: [['day', [1]]]
							}
						}],

						selected: 2,
					},
					exporting: {
						enabled: false
					},
					xAxis: {
						panning: true,
						zoomType: false,
						pinchType: false,
						scrollablePlotArea: {
							scrollPositionX: 1
						},
						crosshair: {
							snap: false,
						},
						ordinal: false,
					},
					yAxis: [{
						labels: {
							align: 'left',
							x: 3,
							format: '{value:.6f}'
						},
						crosshair: {
							snap: false,
							label: {
								enabled: true,
								format: '{value:.6f}'
							}
							
						},
						height: '70%',
						resize: {
							enabled: false
						}
					}, {
						labels: {
							align: 'left',
							x: -3,
							enabled: false,
							format: '{value:.6f}'
						},
						crosshair: {
							snap: false,
							label: {
								enabled: true,
								format: '{value:.6f}'
							}
							
						},
						top: '70%',
						height: '30%',
					}],
					tooltip: {
						split: true,
					},
					navigator: {
						enabled: false
					},

					scrollbar: {
						enabled: false
					},
					series: [{
						type: 'candlestick',
						allowPointSelect: true,
						name: this.$route.params.id.split('_')[0].toUpperCase(),
						data: this.ohlc,
						maxPointWidth: 10,
						dataGrouping: this.dataGrouping,
						// pointIntervalUnit: 'day',
					}, {
						type: 'column',
						name: 'Volume',
						data: this.volume,
						yAxis: 1,
						maxPointWidth: 10,
						dataGrouping: this.dataGrouping,
						// pointIntervalUnit: 'day',
					}]
				}
			}
		},
		computed: {
			tokenGetAddress() {
				return this.pair.tokens[0]
			},
			tokenGiveAddress() {
				return this.pair.tokens[1]
			},
			ohlc(){
				let ohlc = [];
				this.chartData.forEach(el => {
					ohlc.push([
						el.date, // the date
						+el.open.toFixed(6), // open
						+el.max.toFixed(6), // high
						+el.min.toFixed(6), // low
						+el.close.toFixed(6), // close
					]);
				})
				return ohlc;
			},
			volume(){
				let volume = []
				this.chartData.forEach(el => {
					volume.push([
						el.date, // the date
						+(el.volume / 10**18).toFixed(10) // the volume
					]);
				})
				return volume
			},
			chart() {
				return this.$refs.chart
			},
			
		},
		props: {
			pair: Object,
		},
		watch: {
			pair() {
				const vm = this;
				vm.chartData = [];
				vm.stockOptions.rangeSelector.selected = 2;
				vm.stockOptions.series[0].dataGrouping = vm.dataGrouping[2];
				vm.stockOptions.series[1].dataGrouping = vm.dataGrouping[2];
				vm.updateData(function(){
					setTimeout(vm.updateData, 500)
				});
			},
			ohlc(){
				this.stockOptions.series[0].data = this.ohlc;
			},
			volume(){
				this.stockOptions.series[1].data = this.volume;
			}
		},

		// for update chart with web sockets

		// sockets: {
		// 	trade(trade){
		// 		this.formating(trade);
		// 		let point = [
		// 			trade.date, // the date
		// 			+trade.price.toFixed(6), // open
		// 			+trade.price.toFixed(6), // high
		// 			+trade.price.toFixed(6), // low
		// 			+trade.price.toFixed(6), // close
		// 		];
		// 		let volume = [
		// 			trade.date, // the date
		// 			trade.volume
		// 		];
		// 		this.stockOptions.series[0].push(point);
		// 		this.stockOptions.series[1].push(volume);

		// 	}
		// },
		methods: {
			formating(el){
				const vm = this;
				if(el.tokenGet == vm.tokenGetAddress){
					el.orderType = 'buy'
					el.price = +(el.amountGive / el.amountGet).toFixed(10);
					el.amount = el.amountGet
				}else{
					el.orderType = 'sell'
					el.price = +(el.amountGet / el.amountGive).toFixed(10);
					el.amount = el.amountGive
				}
				el.volume = (el.amount * el.price) / 10**18;
			},
			setRange(zoom_, range_){
				this.zoom = zoom_;
				this.stockOptions.xAxis.range = range_;
			},
			updateData(callback){
				var vm = this
				
				vm.$http.get(`${settings.apiURL}/priceChart?tget=${vm.tokenGetAddress}&tgive=${vm.tokenGiveAddress}&page=0`).then(res => {
					var data = res.data._items

						vm.chartData = data;
						this.stockOptions.series[0].data = this.ohlc;
						this.stockOptions.series[1].data = this.volume;
						try {
							// statements
							callback();
						} catch(e) {
							// statements;
						}
					}
				)
			},
			setHeight(vm){
				vm.stockOptions.chart.height = document.querySelector('.chart__container').offsetHeight;
			},
			setPoitnsEvents(vm){
				vm.stockOptions.plotOptions = {
					series: {
						point:{
							events: {
								mouseOver(event){
									vm.date = event.target.x
									setTimeout(function(){
										var tooltips = document.getElementsByClassName('highcharts-tooltip')[0].innerHTML;

										vm.close = Number(tooltips.split('Close: ')[1].split('</')[0]).toFixed(4);
										vm.open = Number(tooltips.split('Open: ')[1].split('</')[0]).toFixed(4);
										vm.high = Number(tooltips.split('High: ')[1].split('</')[0]).toFixed(4);
										vm.low = Number(tooltips.split('Low: ')[1].split('</')[0]).toFixed(4);
										vm.volumeLegend = Number(tooltips.split('Volume')[1].split('dx="0">')[1].split('</')[0]).toFixed(4);
									},20)
								}
							}
						}
					}
				};
			},
			setButtonsEvents(vm){
				vm.stockOptions.rangeSelector.buttons.forEach((el, i) => {
					el.events = {
						click(event){
							// vm.stockOptions.series[0].dataGrouping = vm.dataGrouping[i];
							// vm.stockOptions.series[1].dataGrouping = vm.dataGrouping[i];
							// vm.stockOptions.xAxis.range = vm.range[i];
							vm.stockOptions.rangeSelector.selected = i;
						}
					}
				})
			},
			setXAxisEvents(vm){
				vm.stockOptions.xAxis.events = {
					afterSetExtremes(e){
						vm.rangeCheker = e.dataMax == e.max;
					}
				}
			}

		},
		created(){
			let vm = this;
			setTimeout(function(){
				vm.setHeight(vm);
				vm.setPoitnsEvents(vm);
				vm.setButtonsEvents(vm);
				vm.setXAxisEvents(vm);
			}, 200)
			setInterval(() => {
				if (vm.rangeCheker) {
					vm.updateData()
				}	
			}, 15000);
			vm.updateData();
		}
	}
</script>
<style lang="scss">
	@import '../_base.scss';
	@import '../highchart.scss';
	.meta{
		padding: 10px;
		font-size: 12px;
		display: flex;
		justify-content: space-between;
		position: absolute;
		top: 0;
		left: 0;
		z-index: 1;

		.zoom-btn{
			background: none;
			color: $white;
			border: none;
			font-weight: bold;
			outline: none;
			cursor: pointer;

			&.active{
				color: $algae-green;
			}
		}
	}
	.chart, .stock{
		flex: 1 100%;
		display: flex;
		flex-direction: column;
		a{
			display: none !important;
		}
	}
	.window__title{
		padding: 0px 14px;
		flex: 1 33px;
	}
	.chart__container{
		position: relative;
		background-color: $black-four;
		padding: 5px;
		box-sizing: border-box;
		flex: 0 100%;
		display: flex;
		flex-direction: column;
	}
	#chartdiv {
		width: 100%;
		height: 200px;
		box-sizing: border-box;
		flex: 1 100%;
	}
</style>