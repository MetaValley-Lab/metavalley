// import ProductsSection from "@/components/ProductsSection";
import ProductsSection from "@/app/components/ProductsSection";

export default async function StartupCreateProductsPage({ params }: PageProps<"/startups/[id]/create-product">) {
  const { id } = await params;

  return <ProductsSection startupId={id} />;
}

