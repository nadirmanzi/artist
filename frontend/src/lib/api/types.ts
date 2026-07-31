/**
 * Standard API error structure.
 */
export interface ApiError {
	success: false;
	code: string;
	detail: string;
	errors: Record<string, string[]>; // Field-based validation errors
}

/**
 * Standard API success structure (optional wrapper, some endpoints return data directly).
 */
export interface ApiSuccess<T> {
	success: true;
	data: T;
}

/**
 * Discriminated union for API return results.
 */
export type ApiResult<T> =
	| { ok: true; status: number; data: T; error: null; headers: Headers }
	| { ok: false; status: number; error: ApiError; data: null; headers: Headers | null };

/**
 * Minimal user representation embedded in other resources.
 */
export interface EmbeddedUser {
	user_id: string;
	full_name: string;
	email: string;
}

/**
 * Standard User Profile as per Section 6 of the API Guide.
 */
export interface UserProfile {
	user_id: string; // UUID
	full_name: string;
	email: string;
	telephone_number: string | null;
	password_changed_at: string; // ISO DateTime
	created_at: string; // ISO DateTime
	updated_at: string; // ISO DateTime
}

/**
 * Response for POST /users/auth/login/
 */
export interface LoginResponse {
	user: {
		user_id: string;
		full_name: string;
		email: string;
	};
}

/**
 * Response for POST /users/management/ (Signup)
 */
export interface SignupResponse {
	user: EmbeddedUser;
}

/**
 * Response for GET /users/management/me/
 */
export interface MeResponse {
	user: UserProfile;
}

/**
 * Pagination Wrapper
 */
export interface PaginatedMetadata {
	count: number;
	next: string | null;
	previous: string | null;
	page: number;
	total_pages: number;
}

export interface PaginatedResponse<T> {
	metadata: PaginatedMetadata;
	items: T[];
}

export interface CatalogFilter {
	name?: string;
	description?: string;
	category?: string;
	medium: string;
	year: number;
	visibility_status?: string;
	price_min?: number | string;
	is_sold: boolean;
	price_max?: number | string;
	created_at_after?: string;
	created_at_before?: string;
	user?: string;
}

/**
 * Catalog Types
 */
export interface Catalog {
	catalog_id: string;
	name: string;
	description: string | null;
	price: string | number;
	category: string | null;
	dimensions: string | null;
	year: number | null;
	is_sold: boolean;
	medium: string | null;
	image: string | null;
	user: EmbeddedUser;
	visibility_status: 'draft' | 'published' | 'archived';
	created_at: string;
	updated_at: string;
}

export interface CatalogResponse {
	catalog: Catalog;
}

export interface CatalogListResponse {
	catalogs: Catalog[];
}

/**
 * Class Types
 */
export interface ClassProgram {
	program_id: string;
	name: string;
	price: string;
	sessions: number;
	includes: string[];
	is_active: boolean;
	created_at: string;
	updated_at: string;
}

export interface StudioClass {
	studio_class_id: string;
	name: string;
	description: string;
	is_active: boolean;
	programs: ClassProgram[];
	created_at: string;
	updated_at: string;
}

export interface ClassListResponse {
	classes: StudioClass[];
}

export interface ClassBooking {
	booking_id: string;
	program: ClassProgram;
	name: string;
	email: string;
	phone_number: string | null;
	is_read: boolean;
	created_at: string;
	updated_at: string;
}

export interface ClassBookingResponse {
	class_booking: ClassBooking;
}

/**
 * Inquiry Types
 */
export interface Inquiry {
	inquiry_id: string;
	catalog: Catalog;
	inquirer_name: string | null;
	inquirer_email: string | null;
	inquirer_phone: string | null;
	is_read: boolean;
	created_at: string;
	updated_at: string;
}

export interface InquiryResponse {
	inquiry: Inquiry;
}

export interface InquiryListResponse {
	inquiries: Inquiry[];
}

export interface ContactInquiry {
	contact_inquiry_id: string;
	name: string;
	email: string;
	phone_number: string | null;
	message: string;
	is_read: boolean;
	created_at: string;
	updated_at: string;
}

export interface ContactInquiryResponse {
	contact_inquiry: ContactInquiry;
}

export interface ContactInquiryListResponse {
	contact_inquiries: ContactInquiry[];
}

export interface CreateContactInquiryRequest {
	name: string;
	email: string;
	phone_number?: string | null;
	message: string;
}

export interface ArtworkInquiry {
	artwork_inquiry_id: string;
	catalog: Catalog;
	name: string;
	email: string;
	phone_number: string | null;
	message: string;
	is_read: boolean;
	created_at: string;
	updated_at: string;
}

export interface ArtworkInquiryResponse {
	artwork_inquiry: ArtworkInquiry;
}

export interface ArtworkInquiryListResponse {
	artwork_inquiries: ArtworkInquiry[];
}

export interface CreateArtworkInquiryRequest {
	catalog_id: string;
	name: string;
	email: string;
	phone_number?: string | null;
	message: string | undefined;
}
