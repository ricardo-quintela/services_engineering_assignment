import { UserData } from "./user";

export interface AppointmentData {
    id: number;
    user: UserData;
    horario: string;
    especialidade: string;
    medico: string;
    estado: "open" | "closed";
}