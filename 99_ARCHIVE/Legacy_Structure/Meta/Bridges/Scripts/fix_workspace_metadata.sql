-- Fix: Update create_user_workspace to store workspace_id in user metadata
-- This allows the mobile app to access the workspace_id via user.user_metadata

CREATE OR REPLACE FUNCTION create_user_workspace()
RETURNS TRIGGER AS $$
DECLARE
  new_workspace_id UUID;
BEGIN
  -- Create workspace
  INSERT INTO workspaces (name, owner_id) 
  VALUES ('My Workspace', NEW.id) 
  RETURNING id INTO new_workspace_id;
  
  -- Create profile
  INSERT INTO profiles (id, email, default_workspace_id) 
  VALUES (NEW.id, NEW.email, new_workspace_id);
  
  -- Update user metadata with workspace_id (for easy access in mobile app)
  UPDATE auth.users 
  SET raw_user_meta_data = jsonb_set(
    COALESCE(raw_user_meta_data, '{}'::jsonb),
    '{default_workspace_id}',
    to_jsonb(new_workspace_id::text)
  )
  WHERE id = NEW.id;
  
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Recreate trigger
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created 
  AFTER INSERT ON auth.users 
  FOR EACH ROW 
  EXECUTE FUNCTION create_user_workspace();
