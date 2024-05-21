import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css";
import { PaymentInfo } from "../interfaces/paymentInfoInterface";

const InfoPayment = ({ infoPayment } : {infoPayment: PaymentInfo;}) => {
    return (
        <>
            {infoPayment.entidade && 
                <div className="p-3">
                    Entidade: {infoPayment.entidade}
                </div>  
            }
            {infoPayment.referencia && 
                <div className="p-3">
                    Referência: {infoPayment.referencia}
                </div>
            }
            {infoPayment.telemovel && 
                <div className="p-3">
                    Telemovel: {infoPayment.telemovel}
                </div>
            }
            <div className="p-3">
                Valor: {infoPayment.valor}
            </div>
        </>
    );
};

export default InfoPayment;