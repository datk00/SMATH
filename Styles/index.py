


def styles(currentTheme, _type):
    programTheme = currentTheme['program']
    if _type == 'input':
        return f"""
            QLineEdit {{
                font-size: 13px;                      
                padding: 5px;                       
                border: 2px solid transparent;      
                border-radius: 8px;               
                background-color: {programTheme['input']['background']};       
                color: {programTheme['input']['color']};                      
            }}
            QLineEdit:disabled {{
                background-color: {programTheme['input']['background']};       
                color: {programTheme['input']['color']};                                     
            }}
        """
    elif _type == 'button':
        return f"""
            QPushButton {{
                font-size: 13px;                      
                padding: 5px;                       
                border: 2px solid transparent;      
                border-radius: 5px;               
                background-color: {programTheme['button']['background']};       
                color: {programTheme['button']['color']};     
            }}

            QPushButton:hover {{
                background-color: {programTheme['button']['background_hover']};
            }}
        """
    elif _type == 'submit':
        return f"""
            QPushButton {{
                font-size: 13px;                      
                padding: 8px;                       
                border: 2px solid transparent;      
                border-radius: 5px;               
                background-color: #66BB6A;       
                color: {currentTheme['light_color']};     
            }}

            QPushButton:hover {{
                background-color: #76D47C;
            }}
        """
    elif _type == 'log_area':
        return f"""
        QTextEdit {{
            font-size: 12px;
            background-color: {programTheme['log-area']['background']};
            border-radius: 8px;
            border: none;
        }}
        LogArea {{
            font-size: 12px;
            background-color: {programTheme['log-area']['background']};
            border-radius: 8px;
            border: none;
        }}
        """
    elif _type == 'combo_box':
        return f"""
        QComboBox {{
            font-size: 14px;
            background-color: {programTheme['input']['background']};
            border: 2px solid transparent;
            padding: 5px;
            border-radius: 8px;

        }}
        QComboBox:focus {{
            border: 2px solid green;
        }}
        """