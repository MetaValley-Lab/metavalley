import { z } from "zod";
import { parsePhoneNumberFromString } from "libphonenumber-js";


export const loginSchema = z.object({
  email: z.email({ message: "Digite um e-mail válido" }),
  password: z.string().min(8, "A senha deve ter no mínimo 8 caracteres.")
})

export type LoginFormData = z.infer<typeof loginSchema>;

export const forgotPasswordSchema = z.object({
  email: z.email({ message: "Digite um e-mail válido" }),
});

export type ForgotPasswordFormData = z.infer<typeof forgotPasswordSchema>;

export const resetPasswordSchema = z
  .object({
    password: z.string().min(8, "A senha deve ter no mínimo 8 caracteres."),
    confirm_password: z.string().min(8, "A senha deve ter no mínimo 8 caracteres."),
  })
  .refine((data) => data.password === data.confirm_password, {
    message: "As senhas não coincidem.",
    path: ["confirm_password"],
  });

export type ResetPasswordFormData = z.infer<typeof resetPasswordSchema>;

export const userRegisterSchema = z.object({
  username: z.string().min(1, 'O nome de usuário é obrigatório.'),
  
  email: z.email('E-mail inválido.'),
  
  password: z.string().min(8, 'A senha deve no mínimo ter 8 caracteres.'),
  confirm_password: z.string().min(8, 'A senha deve no mínimo ter 8 caracteres.'),
  
  phone_number: z.string()
    .describe('Telefone no formato nacional (11 99999-8888) ou internacional (+1 202 555 0123)')
    .superRefine((val, ctx) => {
      // Se não começa com '+', assume 'BR' (Brasil) como padrão, igual ao seu backend
      const defaultRegion = val.startsWith('+') ? undefined : 'BR';
      const phoneNumber = parsePhoneNumberFromString(val, defaultRegion);

      // Valida se o número é realmente existente e válido
      if (!phoneNumber || !phoneNumber.isValid()) {
        ctx.addIssue({
          code: z.ZodIssueCode.custom,
          message: 'Número de telefone inválido.',
        });
      }
    })
    .transform((val) => {
      const defaultRegion = val.startsWith('+') ? undefined : 'BR';
      const phoneNumber = parsePhoneNumberFromString(val, defaultRegion);
      
      // Retorna no formato E.164 (Ex: "+5511999998888"), garantindo paridade total com o Python
      return phoneNumber ? phoneNumber.number : val;
    }),
});

export type RegisterRequest = z.infer<typeof userRegisterSchema>;     // Interface que é enviada para o backend
export type RegisterFormData = z.infer<typeof userRegisterSchema>;    // Interface do que o formulário recebe
