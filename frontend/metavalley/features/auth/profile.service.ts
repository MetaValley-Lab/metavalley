import { apiClient } from "@/lib/api/api-client";
import type { EditProfilePayload, UserProfile } from "./profile.types";

export function getProfile(): Promise<UserProfile> {
  return apiClient<UserProfile>("user/profile");
}

export function updateProfile(payload: EditProfilePayload): Promise<{ message: string }> {
  return apiClient<{ message: string }>("user/edit-profile", {
    method: "PATCH",
    body: JSON.stringify(payload),
  });
}

export function uploadAvatar(file: File): Promise<UserProfile> {
  const formData = new FormData();
  formData.append("file", file);
  return apiClient<UserProfile>("user/avatar", { method: "POST", body: formData });
}