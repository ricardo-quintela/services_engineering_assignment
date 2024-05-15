export interface JwtPayload {
    username: string;
    timestamp: number;
    role: string | null;
}