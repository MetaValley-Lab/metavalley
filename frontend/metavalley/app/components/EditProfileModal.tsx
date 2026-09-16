"use client";

import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import Modal from "./Modal";
import TextField from "./TextField";
import Button from "./Button";
import { editProfileSchema, type EditProfileFormData } from "@/features/auth/profile.schema";
import { updateProfile, uploadAvatar } from "@/features/auth/profile.service";
import type { UserProfile } from "@/features/auth/profile.types";

interface EditProfileModalProps {
  visible: boolean;
  profile: UserProfile | null;
  onHide: () => void;
  onSaved: (profile: UserProfile) => void;
}

export default function EditProfileModal({ visible, profile, onHide, onSaved }: EditProfileModalProps) {
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const { register, reset, handleSubmit, formState: { errors, isSubmitting } } = useForm<EditProfileFormData>({
    resolver: zodResolver(editProfileSchema),
  });

  useEffect(() => {
    if (visible && profile) {
      reset({ username: profile.username ?? "", phone_number: profile.phone_number ?? "" });
    }
  }, [profile, reset, visible]);

  function handleHide() {
    setImageFile(null);
    setSubmitError(null);
    onHide();
  }

  async function onSubmit(data: EditProfileFormData) {
    setSubmitError(null);
    try {
      await updateProfile({ user_name: data.username, phone_number: data.phone_number });
      const updatedProfile = imageFile ? await uploadAvatar(imageFile) : { ...profile, username: data.username } as UserProfile;
      onSaved(updatedProfile);
      handleHide();
    } catch (error) {
      console.error("Erro ao editar perfil:", error);
      setSubmitError("Não foi possível salvar o perfil agora.");
    }
  }

  return (
    <Modal visible={visible} onHide={handleHide} title="Editar perfil">
      <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-4">
        <div>
          <TextField id="username" label="Nome de usuário" {...register("username")} />
          {errors.username && <p className="mt-1 text-xs text-red-500">{errors.username.message}</p>}
        </div>
        <div>
          <TextField id="phone_number" label="Número de telefone" type="tel" {...register("phone_number")} />
          {errors.phone_number && <p className="mt-1 text-xs text-red-500">{errors.phone_number.message}</p>}
        </div>
        <div>
          <label htmlFor="profile-image" className="mb-1 block text-sm font-medium text-gray-700">Foto de perfil</label>
          <input id="profile-image" type="file" accept="image/jpeg,image/png,image/webp" onChange={(event) => setImageFile(event.target.files?.[0] ?? null)} className="block w-full text-sm text-gray-600" />
        </div>
        {submitError && <p className="text-sm text-red-500">{submitError}</p>}
        <Button label={isSubmitting ? "Salvando..." : "Salvar alterações"} type="submit" disabled={isSubmitting} />
      </form>
    </Modal>
  );
}