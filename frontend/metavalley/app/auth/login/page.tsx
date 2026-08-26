import BasicDemo from "@/app/components/BasicButtonDemo";
import InputTextDemo from "@/app/components/InputTextDemo";
import Image from "next/image";

export default function LoginPage() {
    return (
        <div className="flex justify-center w-full min-h-screen p-6 gap-4">
            <div className="w-full h-full bg-[#D9D9D9]">
                <Image 
                    src="/image"
                    width={500}
                    height={600}
                    alt="imagem promocional"
                    
                />
            </div>

            <div className="w-full flex justify-center items-center">
                <form>
                    <h2 className="text-4xl text-center font-bold mb-2">Seja Bem-vindo</h2>
                    <p className="text-xs text-gray-400 text-center mb-2">Acesse suas startups e a valide suas ideias</p>
                    <div className="flex flex-col gap-4 mb-6">
                        <InputTextDemo id="E-mail" ariaDescribedBy="email" />
                        <InputTextDemo id="Senha" ariaDescribedBy="senha" />
                    </div>

                    <BasicDemo label="Enviar" />
                </form>
            </div>
        </div>
    )
}