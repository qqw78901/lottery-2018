/**
 * Created by zuowenqi on 2018/2/2 0002
 */
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

    static addAwards(award_name, award_capacity) {
        award_capacity *= 1;
        return this.fetch('/add_award', {
            award_name, award_capacity
        });
    }

    static removeAwards(award_id) {
        return this.fetch('/remove_award', {
            award_id
        });
    }

    static getAwards() {
        return this.fetch('/awards');
    }

    static setCurrent(id) {
        return new Promise(resolve => {
            let prev = localStorage.getItem('current_award') || '';
            localStorage.setItem('prev_award', prev);
            localStorage.setItem('current_award', id);
            resolve(localStorage.getItem('current_award'));
        })
    }

    static getCurrent() {
        return localStorage.getItem('current_award');
    }
}

$(function () {
    $('#add').click(e => {
        layer.open({
            title: '增加',
            content: `
<div>奖品名<input type="text" id="addname"></div>
<div>数&emsp;量<input type="text" id="addnum"></div>
`,
            yes: function (index) {
                let name = $('#addname').val();
                let num = $('#addnum').val();
                BS.addAwards(name, num).then(resp => {
                    console.log(resp);
                    flushAwards();
                    if (resp.status === 200) {
                        layer.close(index);
                    } else {
                        alert(resp.msg);
                    }
                });
            }
        });
    });
    $('#reset').click(e => {
        layer.confirm('确定要重置吗', (index) => {
            BS.fetch('/reset').then(resp => {
                if (resp.status === 200) {
                    layer.close(index);
                    window.location.reload(1);
                }
            });
        });
    });
    $(document).on('click', '.js-set', e => {
        let aid = $(e.target).data('aid');
        let $lis = $('#awardList').find('li');
        BS.setCurrent(aid).then(() => {
            $lis.removeClass('cur');
            $(e.target).closest('li').addClass('cur');
        })
    }).on('click', '.js-remove', e => {
        layer.confirm('确认要删除该项？', () => {
            let aid = $(e.target).data('aid');
            let loadIndex= layer.load(2);
            BS.removeAwards(aid).then((resp) => {
                if (resp.status === 200) {
                    flushAwards();
                    layer.close(loadIndex)
                } else {
                    layer.close(loadIndex);
                    layer.alert(resp.msg)
                }
            })
        })
    });
    flushAwards()

});

function flushAwards() {
    let currentAward = BS.getCurrent();
    BS.getAwards().then(resp => {
        console.log(resp);
        let ul = '';
        resp.data.forEach((val) => {
            let list = `    
            <li class="${currentAward === val.award_id ? 'cur' : ''}">
                <div class="fr">
                    <a type="radio" class="button button-primary button-rounded button-small js-set" data-aid="${val.award_id}">设置成当前轮</a>
                    <a type="radio" class="button button-caution button-circle js-remove" data-aid="${val.award_id}"><i class="fa fa-trash"></i></a>
                </div>
                <div class="content">
                   奖项名称：${val.award_name}，数量：${val.award_capacity}
                </div>
            </li>`;
            ul += list;
        })
        $('#awardList').html(ul)
    })
}