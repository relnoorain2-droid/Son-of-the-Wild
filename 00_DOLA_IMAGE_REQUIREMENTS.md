# Dola Image Requirement

Dola does not only need local file paths. For skill/pro generation it may ask for direct public image URLs.

## Required URL Format

- Direct image URL only.
- URL should end in `.png`, `.jpg`, `.jpeg`, or `.webp`, or return image data with HTTP 200.
- It must not be a webpage link.
- It must be publicly accessible: no login, no "click to view", no private drive page.
- Signed/expiring URLs are okay only if still valid during generation.
- Good character lock needs at least about 1024 px on the short side.

## Good Upload Hosts

- Imgur direct image link, for example `https://i.imgur.com/xxxx.png`
- Discord CDN direct file link
- Postimages direct image link
- ImgBB direct image link
- GitHub raw file link, for example `https://raw.githubusercontent.com/.../image.png`
- Catbox direct file link
- Public S3/R2 bucket

## How To Send To Dola

Paste one direct URL per character in the Dola chat. Example:

`Lily: https://i.imgur.com/xxxx.png`

Then paste the part prompt.