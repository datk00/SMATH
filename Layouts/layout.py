
from Funcs.ptbn import ptbn 
from Funcs.ptb2 import ptb2
from Funcs.ptb3 import ptb3
from Funcs.hptbn2an import hptbn2an
from Funcs.donvi import donvi
from Funcs.bptbn import bptbn
from Funcs.bptb2 import bptb2
from Funcs.vedothi import vedothi
from Funcs.daoham import daoham
from Funcs.nguyenham import nguyenham
from Funcs.dt3d import dt3d


PATH_IMAGES = '../Images'
LAYOUTS = [
    {
        'type': 'button',
        'content': 'Phương trình',
        'icon': {
            'path': f'{PATH_IMAGES}/ptbn_light.png',
            'size': [30, 30]
        },
        '_object': None,
        'action': 'phuong_trinh',
        'active': False,
        'children': [
            {
                'type': 'button',
                'content': 'Phương trình bậc nhất',
                'icon': {
                    'path': f'{PATH_IMAGES}/.png',
                    'size': [30, 30]
                },
                'handleProgram': ptbn
            },
            {
                'type': 'button',
                'content': 'Phương trình bậc hai',
                'icon': {
                    'path': f'{PATH_IMAGES}/.png',
                    'size': [30, 30]
                },
                'handleProgram': ptb2
            },
             {
                'type': 'button',
                'content': 'Phương trình bậc ba',
                'icon': {
                    'path': f'{PATH_IMAGES}/.png',
                    'size': [30, 30]
                },
                'handleProgram': ptb3
            },
            {
                'type': 'button',
                'content': 'Phương trình bậc nhất hai ẩn',
                'icon': {
                    'path': f'{PATH_IMAGES}/.png',
                    'size': [30, 30]
                },
                'handleProgram': hptbn2an
            },
                {
                'type': 'button',
                'content': 'Đổi đơn vị',
                'icon': {
                    'path': f'{PATH_IMAGES}/.png',
                    'size': [30, 30]
                },
                'handleProgram': donvi
            },
        ]
    },
    {
        'type': 'button',
        'content': 'Bất phương trình',
        'icon': {
            'path': f'{PATH_IMAGES}/bptbn.png',
            'size': [30, 30]
        },
        '_object': None,
        'action': 'bat_phuong_trinh',
        'active': False,
        'children': [
            {
                'type': 'button',
                'content': 'Bất phương trình bậc nhất',
                'icon': {
                    'path': f'{PATH_IMAGES}/.png',
                    'size': [30, 30]
                },
                'handleProgram': bptbn
            },
            {
                'type': 'button',
                'content': 'Bất phương trình bậc hai',
                'icon': {
                    'path': f'{PATH_IMAGES}/.png',
                    'size': [30, 30]
                },
                'handleProgram': bptb2

            },
        ]
    },
    {
        'type': 'button',
        'content': 'Đồ thị tổng hợp',
        'icon': {
            'path': f'{PATH_IMAGES}/dtth_light.png',
            'size': [30, 30]
        },
        '_object': None,
        'action': 'do_thi_tong_hop',
        'active': False,
        'children': [
            {
                'type': 'button',
                'content': 'Vẽ đồ thị',
                'icon': {
                    'path': f'{PATH_IMAGES}/.png',
                    'size': [30, 30]
                },
                'handleProgram': vedothi

            },
            {
                'type': 'button',
                'content': 'Minh họa đạo hàm',
                'icon': {
                    'path': f'{PATH_IMAGES}/.png',
                    'size': [30, 30]
                },
                'handleProgram': daoham

            },
              {
                'type': 'button',
                'content': 'Minh họa nguyên hàm',
                'icon': {
                    'path': f'{PATH_IMAGES}/.png',
                    'size': [30, 30]
                },
                'handleProgram': nguyenham

            },
              {
                'type': 'button',
                'content': 'Đồ thị 3D',
                'icon': {
                    'path': f'{PATH_IMAGES}/.png',
                    'size': [30, 30]
                },
                'handleProgram': dt3d

            },
        ]
    },
 
    
]