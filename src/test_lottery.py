#! /usr/bin/python3
# -*- coding:utf-8 -*-

import unittest
from . import lottery as l
import time


class LotteryTestCase(unittest.TestCase):
    def setUp(self):
        print('开始测试', time.strftime('%Y-%m-%d(%a)%H:%M:%S'))
        l.reset()
        self._users = [
            {
                "uid": "G0001",
                "name": "谷歌",
                "award_id": None,
                "role": 0
            },
            {
                "uid": "G0002",
                "name": "百度",
                "award_id": None,
                "role": 1
            },
            {
                "uid": "G0003",
                "name": "搜狗",
                "award_id": None,
                "role": 2
            },
            {
                "uid": "G0004",
                "name": "360",
                "award_id": None,
                "role": 3
            },
            {
                "uid": "G0005",
                "name": "亚马逊",
                "award_id": None,
                "role": 1
            }
        ]

        self._awards = [
                {
                    "award_name": "三等奖(一)",
                    "award_size": 2,
                    "award_capacity": 2
                },
                {
                    "award_name": "三等奖(二)",
                    "award_size": 2,
                    "award_capacity": 2
                },
                {
                    "award_name": "二等奖",
                    "award_size": 2,
                    "award_capacity": 2
                },
                {
                    "award_name": "一等奖",
                    "award_size": 2,
                    "award_capacity": 2
                },
                {
                    "award_name": "特等奖",
                    "award_size": 2,
                    "award_capacity": 2
                }
            ]
        l.add_users(self._users)
        l.add_awards(self._awards)
        for id, award in enumerate(self._awards):
            award['award_id'] = id

    def tearDown(self):
        print('结束测试', time.strftime('%Y-%m-%d(%a)%H:%M:%S'))

    def test_users(self):
        self.assertCountEqual(self._users, l.users()['data'])
        for user in l.users()['data']:
            self.assertTrue(user in self._users)

    def test_draw_lottery(self):
        l.run()
        dlr = l.draw_lottery(0)
        self.assertEqual(dlr['status'], 200)
        for lucky in l.lucky_users(0)['data']:
            self.assertTrue(lucky in dlr['data'])
            print('中奖用户为：', lucky)
        for unlucky in l.luckless_users()['data']:
            for lucky in dlr['data']:
                self.assertNotEqual(lucky['uid'], unlucky['uid'])
        self.assertEqual(len(l.users()['data']), len(l.lucky_users(0)['data']) + len(l.luckless_users()['data']))

    def test_awards(self):
        l.add_awards([{'award_name': "BOSS奖励", 'award_capacity': 1}])
        self.assertEqual(6, len(l.awards()['data']))

    def test_award(self):
        award = l.award(3)
        self.assertEqual('一等奖', award['data']['award_name'])

    def test_update(self):
        l.update('G0004', 3)
        ok = False
        for u in l.lucky_users(3)['data']:
            if u['uid'] == 'G0004':
                ok = True
                break
        self.assertTrue(ok)

    def test_revoke(self):
        l.update('G0004', 3)
        l.revoke('G0004')
        ok = False
        for u in l.lucky_users(3)['data']:
            if u['uid'] == 'G0004':
                ok = True
                break
        self.assertFalse(ok)


if __name__ == '__main__':
    unittest.main()
