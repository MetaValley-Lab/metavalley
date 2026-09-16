export interface UserProfile {
  id: string;
  username: string | null;
  phone_number: string | null;
  avatar_url: string | null;
}

export interface EditProfilePayload {
  user_name?: string;
  phone_number?: string;
}