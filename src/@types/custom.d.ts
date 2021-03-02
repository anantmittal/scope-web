declare module '*.png' {
    const content: any;
    export default content;
}

// NodeJS overrides
declare function setTimeout(callback: () => void, ms: number): number;
declare function clearTimeout(timeoutId: number): void;
