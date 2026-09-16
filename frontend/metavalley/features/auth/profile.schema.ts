import { z } from "zod";
import { parsePhoneNumberFromString } from "libphonenumber-js";

export const editProfileSchema = z.object({
  username: z.string().min(1, "O nome de usuário é obrigatório."),
  phone_number: z.string().superRefine((value, context) => {
    const phone = parsePhoneNumberFromString(value, value.startsWith("+") ? undefined : "BR");
    if (!phone || !phone.isValid()) {
      context.addIssue({ code: z.ZodIssueCode.custom, message: "Número de telefone inválido." });
    }
  }),
});

export type EditProfileFormData = z.infer<typeof editProfileSchema>;