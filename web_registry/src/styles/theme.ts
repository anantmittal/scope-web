import { ThemeOptions } from '@material-ui/core/styles/createMuiTheme';
import { indigo } from '@mui/material/colors';
import { createTheme } from '@mui/material/styles';

export const themeOptions: ThemeOptions = {
    palette: {
        type: 'light',
        primary: {
            main: '#3f51b5',
        },
        secondary: {
            main: '#f50057',
        },
    },
    typography: {
        body1: {
            fontSize: '1rem',
            lineHeight: 1.15,
        },
        body2: {
            fontSize: '1rem',
            lineHeight: 1.05,
        },
        fontSize: 12,
    },
    spacing: 4,
    props: {
        MuiList: {
            dense: true,
        },
        MuiMenuItem: {
            dense: true,
        },
        MuiTable: {
            size: 'small',
        },
        MuiButton: {
            size: 'small',
        },
        MuiButtonGroup: {
            size: 'small',
        },
        MuiCheckbox: {
            size: 'small',
        },
        MuiFab: {
            size: 'small',
        },
        MuiFormControl: {
            margin: 'dense',
            size: 'small',
        },
        MuiFormHelperText: {
            margin: 'dense',
        },
        MuiIconButton: {
            size: 'small',
        },
        MuiInputBase: {
            margin: 'dense',
        },
        MuiInputLabel: {
            margin: 'dense',
        },
        MuiRadio: {
            size: 'small',
        },
        MuiSwitch: {
            size: 'small',
        },
        MuiTextField: {
            margin: 'dense',
            size: 'small',
        },
    },
};

declare module '@mui/material/styles' {
    interface Theme {
        customPalette: {
            subtle: React.CSSProperties['color'];
            label: React.CSSProperties['color'];
            discrete10: string[];
            scoreColors: { [key: string]: string };
        };
        customSizes: {
            contentsMenuWidth: number;
            headerHeight: number;
            footerHeight: number;
        };
    }
    interface ThemeOptions {
        customPalette: {
            subtle: React.CSSProperties['color'];
            label: React.CSSProperties['color'];
            discrete10: string[];
            scoreColors: { [key: string]: string };
        };
        customSizes: {
            contentsMenuWidth: number;
            headerHeight: number;
            footerHeight: number;
        };
    }
}

export default function createAppTheme() {
    return createTheme({
        palette: {
            primary: {
                main: '#3f51b5',
            },
            secondary: {
                main: '#f50057',
            },
        },
        typography: {
            body1: {
                fontSize: '1rem',
                lineHeight: 1.15,
            },
            fontSize: 12,
        },
        spacing: 4,
        customPalette: {
            subtle: '#eeeeee',
            label: '#00000088',
            discrete10: [
                '#1f77b4',
                '#ff7f0e',
                '#2ca02c',
                '#d62728',
                '#9467bd',
                '#8c564b',
                '#e377c2',
                '#7f7f7f',
                '#bcbd22',
                '#17becf',
            ],
            scoreColors: {
                bad: '#bf2e2e',
                warning: '#ffbf00',
                good: '#20ab41',
                unknown: '#fafafa',
            },
        },
        customSizes: {
            contentsMenuWidth: 300,
            headerHeight: 48,
            footerHeight: 48,
        },
        components: {
            MuiList: {
                defaultProps: {
                    dense: true,
                },
            },
            MuiMenuItem: {
                defaultProps: {
                    dense: true,
                },
            },
            MuiTable: {
                defaultProps: {
                    size: 'small',
                },
            },
            MuiButton: {
                defaultProps: {
                    size: 'small',
                },
            },
            MuiButtonGroup: {
                defaultProps: {
                    size: 'small',
                },
            },
            MuiCheckbox: {
                defaultProps: {
                    size: 'small',
                },
            },
            MuiFab: {
                defaultProps: {
                    size: 'small',
                },
            },
            MuiFormControl: {
                styleOverrides: {
                    root: {
                        paddingBottom: '24px',
                    },
                },
                defaultProps: {
                    margin: 'dense',
                    size: 'small',
                },
            },
            MuiFormControlLabel: {
                styleOverrides: {
                    label: {
                        fontSize: 14,
                        paddingBottom: 0,
                    },
                },
            },
            MuiFormHelperText: {
                defaultProps: {
                    margin: 'dense',
                },
            },
            MuiFormLabel: {
                styleOverrides: {
                    root: {
                        color: indigo[500],
                        textTransform: 'uppercase',
                        fontWeight: 700,
                    },
                },
            },
            MuiIconButton: {
                defaultProps: {
                    size: 'small',
                },
            },
            MuiInput: {
                styleOverrides: {
                    input: {
                        padding: '6px 12px',
                    },
                    inputMultiline: {
                        padding: '0 12px',
                    },
                    underline: {
                        background: '#fafafa',
                    },
                },
            },
            MuiInputBase: {
                defaultProps: {
                    margin: 'dense',
                },
            },
            MuiInputLabel: {
                defaultProps: {
                    margin: 'dense',
                },
                styleOverrides: {
                    shrink: {
                        transform: 'translate(0)',
                        fontSize: 14,
                        paddingBottom: 6,
                    },
                    formControl: {
                        transform: 'translate(0)',
                        fontSize: 14,
                        paddingBottom: 6,
                    },
                },
            },
            MuiRadio: {
                defaultProps: {
                    size: 'small',
                },
            },
            MuiSwitch: {
                defaultProps: {
                    size: 'small',
                },
            },
            MuiTextField: {
                defaultProps: {
                    margin: 'dense',
                    size: 'small',
                },
            },
        },
    });
}
