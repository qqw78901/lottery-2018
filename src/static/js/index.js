$(document).ready(function () {
    new Index();
});

class BS {
    constructor() {

    }

    static fetch(url, data, type) {
        return new Promise((resolve) => {
            $.ajax({
                type: type ? type : 'GET',
                data: data ? data : {},
                url,
                success(resp) {
                    resolve(resp)
                }
            })
        })

    }

    static run() {
        return this.fetch('/run');
    }

    static stopAndResult(award_id) {
        return this.fetch('/draw_lottery', {award_id});
    }

    static getLucklessUsers() {
        return this.fetch('/luckless_users');
    }

    static getLuckyUsers() {
        return this.fetch('/lucky_users');
    }

    static getAwards() {
        return this.fetch('/awards');
    }

    static getAward(award_id) {
        return this.fetch('/award', {
            award_id
        });
    }

    static getUsers() {
        return this.fetch('/users');
    }


}

class Tag {
    constructor(entries) {
        this.id = 'myCanvas';
        this.entries = entries;
        this.createCanvas();
    }

    createHTML() {
        let html = ['<ul>'];
        $(this.entries).each((i, val) => {
            let color = val.award_id ? 'yellow' : 'white';
            html.push(`<li><a href="javascript:void(0)" style="color: ${color};" data-uid="${val.uid}" data-role="${val.role}">${val.name}</a></li>`);
            // html.push(`<li><a href="#" style="color:${color};">' + item.name + '</a></li>`);
        });
        html.push('</ul>');
        return html.join('');
    };

    static speed() {
        return [0.1 * Math.random() + 0.01, -(0.1 * Math.random() + 0.01)];
    };

    createCanvas() {
        let canvas = document.createElement('canvas');
        canvas.id = this.id;
        canvas.width = 1024;
        canvas.height = 600;
        document.getElementById('holder').appendChild(canvas);
        this.canvas = canvas;
        canvas.innerHTML = this.createHTML();
        TagCanvas.Start('myCanvas', '', {
            textColour: null,
            initial: Tag.speed(),
            dragControl: 1,
            textHeight: 14
        });
    }

    markYellow(users) {
        let color = 'yellow';
        for (let user of users) {
            $(this.canvas).find(`[data-uid=${user.uid}]`).css('color', color);
        }
        TagCanvas.Reload(this.id);
    }

    fast() {
        TagCanvas.SetSpeed(this.id, [5, 1]);
    }

    stop() {
        TagCanvas.SetSpeed(this.id, Tag.speed());
        TagCanvas.Reload(this.id);
    }
}

class Index {
    constructor() {
        this.running = false;
        this.currentAward = '';
        this.entries = [];
        this.buildCloud().then(() => {
            this.canvas3DTagCloud = new Tag(this.entries)
        });
        this.bindEvent();
        this.initVisualSocket();
    }

    buildCloud() {
        return BS.getUsers().then((resp) => {
            console.log(resp);
            this.entries = resp.data;
        })
    }

    initVisualSocket() {
        let tempAwardId = '';
        setInterval(() => {
            tempAwardId = localStorage.getItem('current_award');
            if (this.currentAward !== tempAwardId) {
                /*change*/
                // window.location.reload(1);
                this.currentAward = tempAwardId;
                this.refreshCurrentAward();
            }
        }, 1000);
    }

    refreshCurrentAward() {
        if (this.currentAward === '') return;
        BS.getAward(this.currentAward).then((resp) => {
            console.log(resp);
            if (resp.status === 200) {
                let awardInfo = resp.data;
                $('#currentAwardName').html(awardInfo.award_name);
                $('#currentTimes').html(awardInfo.award_capacity);
            }

        })
    }


    bindEvent() {
        $('#start').click(() => {
            if (this.running) {
                alert('正在抽奖');
                return;
            }
            this.canvas3DTagCloud.fast();
            BS.run().then(resp => {
                console.log(resp);
                this.running = true;
            });
        });
        $('#end').click(() => {
            if (!this.running) {
                return;
            }
            console.log('click');
            BS.stopAndResult(this.currentAward).then(resp => {
                console.log(resp);
                if (resp.status === 200) {
                    this.stopLottery(resp.data);
                    this.running = false;
                }else{
                    this.running=false;
                    this.canvas3DTagCloud.stop();
                    layer.alert(resp.msg);

                }
            });
        });
        $(document).on('click', function () {
            $('#result').hide();
            $('.holder').removeClass('mask');
        });
        $('#luckyUsers').click(() => {
            this.list();
        });

    }

    stopLottery(data) {
        this.canvas3DTagCloud.stop();
        this.currentlist(data);
        this.canvas3DTagCloud.markYellow(data)
    }

    /**
     * 当前轮结果
     * @param data
     */
    currentlist(data) {
        // let offset = $(".holder").offset();
        let DOM = '';
        for (let user of data) {
            DOM += `<span class="${(user.role === 2 || user.role === 3) ? 'sp animated flash' : ''}"><i>${user.name}<br>${user.uid}</i></span>`;
        }
        DOM += ``;
        $('#result').show().html(DOM);
        setTimeout(function () {
            $('.holder').addClass('mask');
        }, 10);
    }

    /**
     * 所有结果
     */
    list() {
        let offset = $(".holder").offset();
        let awards = {};
        let load = layer.load(2);
        BS.getAwards().then(resp => {
            resp.data.map((val) => {
                console.log(val);
                if (typeof awards[val.award_id] === "undefined") {
                    awards[val.award_id] = {};
                }
                awards[val.award_id].name = val.award_name;
                awards[val.award_id].data = [];

            })

        }).then(() => {
            return BS.getLuckyUsers().then(resp => {
                resp.data.map(val => {
                    awards[val.award_id].data.push(val)
                })
            });
        }).then(() => {
            layer.close(load);
            console.log(awards);
            let content = ``;
            for (let key of Object.keys(awards)) {
                let award = awards[key];
                let lisArray = award.data.map((data) => {
                    return `<li class="${data.role == 2 || data.role == 3 ? 'sp' : ''}">${data.name}<span>【${data.uid}】</span></li>`
                });
                if(lisArray.length!==0){
                    content += `
                                <section>
                                    <h5>${award.name}</h5>
                                    <ul>
                                    ${lisArray.join("")}
                                    </ul>
                                </section>
                    `;
                }

            }
            layer.open({
                type: 1,
                area: ['1024px','600px'],
                skin: 'layui-layer-lan', //样式类名
                offset: [offset.top, offset.left],
                closeBtn: 1, //不显示关闭按钮
                anim: 3,
                title: '所有中奖名单',
                shadeClose: false, //开启遮罩关闭
                content: `
<div class="luckerList">${content}
</div>`
            });
        });
    }
}

