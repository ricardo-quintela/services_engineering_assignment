import { UserData } from "./user";

export interface AppointmentData {
    id: number;
    user: UserData;
    data_appointment: string;
    hora: number;
    especialidade: number;
    medico: string;
    estado: "open" | "closed" | "ongoing" | "payed";
}